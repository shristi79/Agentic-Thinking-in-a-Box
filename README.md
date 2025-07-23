# AI-Powered GitHub Issue Assistant

## Overview
This project is a web application that leverages AI to analyze GitHub issues in real time. Enter a public GitHub repository URL and an issue number, and the app will fetch the issue details and comments, analyze them using a Large Language Model (LLM) via Hugging Face, and return a structured summary and classification.

---

## Features
- **Input UI:** Enter a GitHub repo URL and issue number.
- **Backend:** Python Flask API fetches issue data and interacts with the LLM.
- **AI Core:** Uses Hugging Face's OpenAI-compatible API (e.g., DeepSeek, Mistral, etc.) for analysis.
- **Frontend:** Streamlit app for rapid prototyping and clean display.
- **Output:** Structured JSON with summary, type, priority, suggested labels, and potential impact.

---

## Tech Stack
- **Backend:** Python (Flask)
- **Frontend:** Streamlit
- **LLM:** Hugging Face Inference API (OpenAI-compatible)

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd SeedlingLabs
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root with your Hugging Face API token:
```
HUGGINGFACE_API_TOKEN=hf_your_token_here
```
- **Never commit your `.env` file to version control.**
- Add `.env` to your `.gitignore`.

### 4. Run the Backend (Flask)
```sh
cd backend
python app.py
```

### 5. Run the Frontend (Streamlit)
Open a new terminal:
```sh
cd frontend
python -m streamlit run app.py
```

---

## Usage
1. Open the Streamlit app in your browser (usually at [http://localhost:8501](http://localhost:8501)).
2. Enter a public GitHub repository URL (e.g., `https://github.com/facebook/react`).
3. Enter an issue number (e.g., `1`).
4. Click **Analyze Issue**.
5. View the AI-generated structured analysis.

---

## Security Notes
- **Do not commit your `.env` file or any secrets to GitHub.**
- If you accidentally pushed a secret, revoke it immediately and follow [GitHub's guide on removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

---

## Customization
- You can change the LLM model by editing the model name in `backend/app.py`.
- To support private repos, you would need to add GitHub authentication (not included in this version).

---

## License
This project is for educational and demonstration purposes. 