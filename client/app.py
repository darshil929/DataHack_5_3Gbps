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


st.subheader("Upload Your Resume (PDF)")
resume_upload = st.file_uploader("Choose a PDF file", type=["pdf"])

if resume_upload:
    st.write("Resume Uploaded Successfully!")
    

    resume_folder = 'resumes'
    os.makedirs(resume_folder, exist_ok=True)
    temp_resume_path = os.path.join(resume_folder, "temp_resume.pdf")
    with open(temp_resume_path, "wb") as temp_file:
        temp_file.write(resume_upload.read())
    

    st.write("Analyzing the resume...") 


    resume_file = temp_resume_path
    headers = {'Authorization': 'Your-Authorization-Token'}

    response = requests.post(
        url="http://localhost:5000/parse_resume", 
        files={'resume': open(resume_file, 'rb')}
    )

    if response.status_code == 200:
        data = response.json()
        
        st.write("Resume analysis complete.")
        st.write(data.get("message", "Data saved successfully."))
    else:
        st.write(f"Resume analysis failed with status code {response.status_code}: {response.text}")


st.subheader("Project Management")

collaborative_workspace = st.checkbox("Collaborative Workspace")
multi_lingual_support = st.checkbox("Multi-Lingual Support")
analytics_dashboard = st.checkbox("Advanced Analytics and Engagement Dashboard")

st.subheader("Skill Recommendations for Jobs")

job_description = st.text_area("Enter Job Description")
if st.button("Get Project Recommendations"):

    recommendations_url = "http://localhost:5001/recommend_skills" 

    if job_description:
        response = requests.post(recommendations_url, json={"job_description": job_description})

        if response.status_code == 200:
            top_missing_skills = response.json()
            if top_missing_skills:
                st.write("Top 5 recommended skills to improve your portfolio:")
                for i, skill in enumerate(top_missing_skills, 1):
                    st.write(f"{i}. {skill}")
            else:
                st.write("No skills recommended for the given job description.")
        else:
            st.write(f"Skill recommendation failed with status code {response.status_code}: {response.text}")
    else:
        st.write("Please enter a job description.")