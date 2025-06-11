# AI Content Checker

This project provides a simple web interface for users to input a message, which is then evaluated by an AI agent to determine if it passes or fails certain criteria.

## Project Structure

```
.
├── .env                # Environment variables for backend
├── .venv/              # Python virtual environment (not included in repo)
├── content_evaluator.py # Python module for evaluating content
├── main.py             # FastAPI backend server
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates (index.html for the web UI)
└── README.md           # Project documentation
```

## Features
- Simple web interface with a message box
- AI agent evaluates user input and returns Pass/Fail
- FastAPI backend for evaluation logic

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-project-directory>
```

### 2. Set Up Python Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root if needed (see `.env.example` if available).

### 4. Run the Backend Server
```bash
uvicorn main:app --reload
```
The server will start at [http://localhost:8000](http://localhost:8000)

### 5. Access the Web Interface
- Make sure `index.html` is in the `templates/` directory.
- Open your browser and go to [http://localhost:8000](http://localhost:8000)
- Enter your message and click "Check" to see if it passes or fails.

## API Endpoint
- `POST /evaluate` — Accepts JSON `{ "content": "your message" }` and returns `{ "pass": true/false, ... }`

## Development Notes
- To serve static HTML only, you can use Python's built-in HTTP server:
  ```bash
  python3 -m http.server 8000
  ```
- For full AI evaluation, use the FastAPI backend as described above.

## License
MIT 