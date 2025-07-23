import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse
import json
import re
from flask import Flask, request, jsonify

load_dotenv()
app = Flask(__name__)

GITHUB_API_BASE = "https://api.github.com"

# Set up OpenAI-compatible Hugging Face client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HUGGINGFACE_API_TOKEN"],
)

@app.route('/analyze_issue', methods=['POST'])
def analyze_issue():
    data = request.get_json()
    repo_url = data.get('repo_url')
    issue_number = data.get('issue_number')
    try:
        # Parse owner and repo from URL
        path_parts = urlparse(repo_url).path.strip('/').split('/')
        if len(path_parts) < 2:
            return jsonify({'error': 'Invalid repository URL.'}), 400
        owner, repo = path_parts[0], path_parts[1]
        # Fetch issue details
        issue_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues/{issue_number}"
        issue_resp = requests.get(issue_url)
        if issue_resp.status_code != 200:
            return jsonify({'error': f'Issue not found or repo invalid. ({issue_resp.status_code})'}), 404
        issue_data = issue_resp.json()
        # Fetch comments
        comments_url = issue_data.get('comments_url')
        comments_resp = requests.get(comments_url)
        comments = comments_resp.json() if comments_resp.status_code == 200 else []
        # Prepare data for LLM
        title = issue_data.get('title')
        body = issue_data.get('body')
        comments_text = '\n'.join([c.get('body') for c in comments if c.get('body')])
        # Compose prompt
        prompt = f"""
You are an AI assistant. Analyze the following GitHub issue and return a JSON object in this format:
{{
  \"summary\": \"A one-sentence summary of the user's problem or request.\",
  \"type\": \"Classify the issue as one of the following: bug, feature_request, documentation, question, or other.\",
  \"priority_score\": \"A score from 1 (low) to 5 (critical), with a brief justification for the score.\",
  \"suggested_labels\": [\"An array of 2-3 relevant GitHub labels (e.g., 'bug', 'UI', 'login-flow').\"],
  \"potential_impact\": \"A brief sentence on the potential impact on users if the issue is a bug.\"
}}

Issue Title: {title}
Issue Body: {body}
Comments: {comments_text}
"""
        # Call Hugging Face's OpenAI-compatible API
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1:novita",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.2
        )
        ai_content = response.choices[0].message.content
        match = re.search(r'\{[\s\S]*\}', ai_content)
        if match:
            ai_json = match.group(0)
            try:
                return jsonify(json.loads(ai_json))
            except Exception as e:
                return jsonify({'error': 'Failed to parse AI JSON.', 'ai_content': ai_content}), 500
        else:
            return jsonify({'error': 'No JSON found in AI response.', 'ai_content': ai_content}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 