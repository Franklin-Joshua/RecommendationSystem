# Personalized Recommendation System

Streamlit app powered by the local Ollama `qwen3:4b` model.

## Features
- User profile collection and preference analysis
- Prompt construction and personalized recommendations
- Suitability ranking and explanations
- Feedback-based refinement
- Intent detection
- Save and download recommendations

## Setup (Windows PowerShell)
```powershell
ollama pull qwen3:4b
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run main.py
```
Keep Ollama running. The app uses `http://localhost:11434` by default.

Scores are model-generated estimates, not objective measurements. Review recommendations before relying on them.
