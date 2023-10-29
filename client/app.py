import streamlit as st
import requests
import json

st.set_page_config(
    page_title="AI-Powered Portfolio Management",
    page_icon=":clipboard:",
    layout="wide",
)

main_style = """
    padding: 2rem;
"""

st.write(
    f"""
    <style>
    .reportview-container {{
        {main_style}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("AI-Powered Portfolio Management System")

st.subheader("Upload Your Resume (PDF)")
resume_upload = st.file_uploader("Choose a PDF file", type=["pdf"])

if resume_upload:
    st.write("Resume Uploaded Successfully!")
    
    # Create a dictionary to send the resume file to the parser
    files = {'resume': resume_upload}
    
    # Send the resume for parsing using a POST request to the resume parser API
    parser_url = "http://localhost:5000/parse_resume"  # Replace with the actual URL of the parser API
    response = requests.post(parser_url, files=files)
    
    if response.status_code == 200:
        data = response.json()
        st.write("Resume analysis complete. Extracted data saved.")
    else:
        st.write(f"Resume analysis failed with status code {response.status_code}: {response.text}")

# User-friendly interface to categorize and manage projects
st.subheader("Project Management")

collaborative_workspace = st.checkbox("Collaborative Workspace")
multi_lingual_support = st.checkbox("Multi-Lingual Support")
analytics_dashboard = st.checkbox("Advanced Analytics and Engagement Dashboard")

st.subheader("Project Recommendations")

job_description = st.text_area("Enter Job Description")
if st.button("Get Project Recommendations"):
    # Send the job description to the job recommendation code
    recommendations_url = "http://localhost:5000/recommend_skills"  # Replace with the actual URL of the job recommendation API
    response = requests.post(recommendations_url, json={"job_description": job_description})
    
    if response.status_code == 200:
        top_missing_skills = response.json()
        st.write("Top 5 recommended skills to improve your portfolio:")
        for i, skill in enumerate(top_missing_skills, 1):
            st.write(f"{i}. {skill}")
    else:
        st.write(f"Skill recommendation failed with status code {response.status_code}: {response.text}")
