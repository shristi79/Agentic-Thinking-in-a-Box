import streamlit as st
import requests

st.title("AI-Powered GitHub Issue Assistant")

repo_url = st.text_input("GitHub Repository URL", "https://github.com/facebook/react")
issue_number = st.text_input("Issue Number", "1")

if st.button("Analyze Issue"):
    with st.spinner("Analyzing..."):
        try:
            response = requests.post(
                "http://localhost:5000/analyze_issue",
                json={"repo_url": repo_url, "issue_number": issue_number}
            )
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}") 