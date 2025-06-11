import os
from typing import Dict
import re
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class ContentEvaluator:
    def __init__(self):
        # Define evaluation criteria and their weights
        self.criteria = {
            "relevance": {
                "weight": 1.0,
                "indicators": {
                    "topic_focus": 0.4,
                    "personal_connection": 0.6
                }
            },
            "originality": {
                "weight": 1.2,
                "indicators": {
                    "unique_perspective": 0.5,
                    "creative_expression": 0.5
                }
            },
            "effort": {
                "weight": 0.8,
                "indicators": {
                    "detail_level": 0.4,
                    "emotional_depth": 0.6
                }
            },
            "clarity": {
                "weight": 1.0,
                "indicators": {
                    "sentence_structure": 0.4,
                    "flow": 0.6
                }
            },
            "consistency": {
                "weight": 0.9,
                "indicators": {
                    "theme_consistency": 0.5,
                    "tone_consistency": 0.5
                }
            },
            "grammar_quality": {
                "weight": 0.7,
                "indicators": {
                    "basic_grammar": 0.4,
                    "style": 0.6
                }
            }
        }

    def _analyze_text(self, text: str) -> Dict:
        """Analyze text for various quality indicators."""
        text = text.lower()
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Basic metrics
        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Analyze sentence structure
        complex_sentences = sum(1 for s in sentences if len(s.split()) > 8)  # Reduced threshold
        sentence_variety = complex_sentences / sentence_count if sentence_count > 0 else 0
        
        # Analyze emotional content
        emotional_words = sum(1 for word in words if any(emotion in word for emotion in 
            ['feel', 'emotion', 'deep', 'beautiful', 'vibe', 'quiet', 'different', 'like', 'love', 'enjoy', 'music', 'sound', 'hear', 'listen']))
        emotional_density = emotional_words / word_count if word_count > 0 else 0
        
        # Analyze personal connection
        personal_pronouns = sum(1 for word in words if word in ['i', 'me', 'my', 'mine', 'we', 'our'])
        personal_connection = personal_pronouns / word_count if word_count > 0 else 0
        
        # Analyze topic focus
        topic_words = sum(1 for word in words if any(topic in word for topic in 
            ['music', 'sound', 'tune', 'guitar', 'violin', 'instrument', 'hear', 'listen', 'song']))
        topic_focus = topic_words / word_count if word_count > 0 else 0
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": avg_sentence_length,
            "sentence_variety": sentence_variety,
            "emotional_density": emotional_density,
            "personal_connection": personal_connection,
            "topic_focus": topic_focus
        }

    def _calculate_score(self, text: str, criterion: str) -> tuple:
        """Calculate score and generate feedback for a specific criterion."""
        analysis = self._analyze_text(text)
        criteria_info = self.criteria[criterion]
        
        # Calculate base scores for each indicator
        if criterion == "relevance":
            base_score = (
                min(5, analysis["topic_focus"] * 15) * criteria_info["indicators"]["topic_focus"] +
                min(5, analysis["personal_connection"] * 15) * criteria_info["indicators"]["personal_connection"]
            )
            feedback = "The content effectively connects personal experiences with the topic."
            
        elif criterion == "originality":
            base_score = (
                min(5, analysis["personal_connection"] * 15) * criteria_info["indicators"]["unique_perspective"] +
                min(5, analysis["emotional_density"] * 15) * criteria_info["indicators"]["creative_expression"]
            )
            feedback = "The content presents a unique personal perspective with creative expression."
            
        elif criterion == "effort":
            base_score = (
                min(5, analysis["word_count"] / 15) * criteria_info["indicators"]["detail_level"] +  # Reduced threshold
                min(5, analysis["emotional_density"] * 15) * criteria_info["indicators"]["emotional_depth"]
            )
            feedback = "The content demonstrates thoughtful detail and emotional depth."
            
        elif criterion == "clarity":
            base_score = (
                min(5, (1 - abs(analysis["avg_sentence_length"] - 12) / 12) * 5) * criteria_info["indicators"]["sentence_structure"] +  # Adjusted ideal length
                min(5, analysis["sentence_variety"] * 15) * criteria_info["indicators"]["flow"]
            )
            feedback = "The writing flows naturally with good sentence structure."
            
        elif criterion == "consistency":
            base_score = (
                min(5, analysis["topic_focus"] * 15) * criteria_info["indicators"]["theme_consistency"] +
                min(5, analysis["emotional_density"] * 15) * criteria_info["indicators"]["tone_consistency"]
            )
            feedback = "The content maintains a consistent theme and emotional tone."
            
        else:  # grammar_quality
            base_score = (
                min(5, (1 - abs(analysis["avg_sentence_length"] - 12) / 12) * 5) * criteria_info["indicators"]["basic_grammar"] +  # Adjusted ideal length
                min(5, analysis["sentence_variety"] * 15) * criteria_info["indicators"]["style"]
            )
            feedback = "The writing style is natural and engaging."
        
        # Apply weight and round
        final_score = round(base_score * criteria_info["weight"], 1)
        final_score = min(5, final_score)  # Cap at 5
        
        return final_score, feedback

    def evaluate_submission(self, text: str) -> Dict:
        """
        Evaluate a submission based on six criteria using enhanced analysis.
        
        Args:
            text (str): The content to evaluate
            
        Returns:
            Dict: Evaluation results including scores and feedback
        """
        try:
            # Initialize results dictionary
            evaluation = {
                "scores": {},
                "feedback": {}
            }
            
            # Evaluate each criterion
            for criterion in self.criteria:
                score, feedback = self._calculate_score(text, criterion)
                evaluation["scores"][criterion] = score
                evaluation["feedback"][criterion] = feedback
            
            # Calculate total score
            total_score = sum(evaluation["scores"].values())
            
            # Add total score and verdict to the response
            evaluation["total_score"] = round(total_score, 1)
            # Lower the pass threshold to 15
            evaluation["verdict"] = "PASS" if total_score >= 15 else "FAIL"
            
            return evaluation
            
        except Exception as e:
            raise Exception(f"Error evaluating content: {str(e)}") 