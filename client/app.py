import streamlit as st
import requests
import json
import os

# Create a Streamlit web app
st.set_page_config(
    page_title="AI-Powered Portfolio Management",
    page_icon=":clipboard:",
    layout="wide",
)

# Define page styles with CSS
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

# Uploading Resume File
st.subheader("Upload Your Resume (PDF)")
resume_upload = st.file_uploader("Choose a PDF file", type=["pdf"])

if resume_upload:
    st.write("Resume Uploaded Successfully!")

    # Save the uploaded resume as a temporary file
    resume_folder = 'resumes'  # Create a folder to store the resumes
    os.makedirs(resume_folder, exist_ok=True)
    temp_resume_path = os.path.join(resume_folder, "temp_resume.pdf")
    with open(temp_resume_path, "wb") as temp_file:
        temp_file.write(resume_upload.read())

    # Call resume_parser.py for analysis
    st.write("Analyzing the resume...")

    # Modify the resume_parser.py code to use the uploaded resume
    resume_file = temp_resume_path  # Use the temporary resume file
    headers = {'Authorization': 'Your-Authorization-Token'}

    # Use requests to send the resume for parsing
    response = requests.post(
        url="http://localhost:5000/parse_resume",  # Modify the URL if needed
        files={'resume': open(resume_file, 'rb')}
    )

    if response.status_code == 200:
        data = response.json()

        st.write("Resume analysis complete.")
        st.write(data.get("message", "Data saved successfully."))
    else:
        st.write(
            f"Resume analysis failed with status code {response.status_code}: {response.text}")

# User-friendly interface to categorize and manage projects
st.subheader("Project Management")

collaborative_workspace = st.checkbox("Collaborative Workspace")
multi_lingual_support = st.checkbox("Multi-Lingual Support")
analytics_dashboard = st.checkbox(
    "Advanced Analytics and Engagement Dashboard")

st.subheader("Project Recommendations")

job_description = st.text_area("Enter Job Description")
if st.button("Get Project Recommendations"):
    # Send the job description to the job recommendation code
    # Replace with the actual URL of the job recommendation API
    recommendations_url = "http://localhost:5000/recommend_skills"
    response = requests.post(recommendations_url, json={
                             "job_description": job_description})

    if response.status_code == 200:
        top_missing_skills = response.json()
        st.write("Top 5 recommended skills to improve your portfolio:")
        for i, skill in enumerate(top_missing_skills, 1):
            st.write(f"{i}. {skill}")
    else:
        st.write(
            f"Skill recommendation failed with status code {response.status_code}: {response.text}")
