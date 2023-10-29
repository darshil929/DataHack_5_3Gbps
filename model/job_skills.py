import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import json 

from flask import Flask, request, jsonify

app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

df = pd.read_csv("./datasets/naukri_data_science_jobs_india (2).csv")

df['all_skills'] = df[['skills', 'skills2', 'skills3', 'skills4', 'skills5', 'skills6', 'skills7', 'skills8']].apply(lambda x: ' '.join(x.dropna()), axis=1)

cv = CountVectorizer(max_features=10000, stop_words='english')
skill_matrix = cv.fit_transform(df['all_skills']).toarray()

cosine_sim_skills = cosine_similarity(skill_matrix)

def recommend_skills(job_description, user_skills):
    job_titles = []
    doc = nlp(job_description)
    for ent in doc.ents:
        if ent.label_ == "JOB_TITLE":
            job_titles.append(ent.text)

    skills_similarity = cosine_similarity(cv.transform([job_description]).toarray(), skill_matrix).flatten()
    
    job_title_similarity = np.array([np.mean([1 if title in df['Job-Title'].iloc[i] else 0 for title in job_titles]) for i in range(len(df))])

    combined_similarity = 0.7 * skills_similarity + 0.3 * job_title_similarity

    sim_scores = list(enumerate(combined_similarity))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    similar_jobs = sim_scores[1:6]

    recommended_skills = []
    for idx, _ in similar_jobs:
        recommended_skills.extend(df['all_skills'].iloc[idx].split())

    missing_skills = list(set(recommended_skills) - set(user_skills))
    
    # Sort the missing skills by their similarity to the job description
    missing_skills_similarity = [combined_similarity[df.index[df['all_skills'].str.contains(skill)].tolist()[0]] for skill in missing_skills]
    top_missing_skills = [skill for _, skill in sorted(zip(missing_skills_similarity, missing_skills), reverse=True)][:5]

    return top_missing_skills

user_skills = []  # Initialize as an empty list
with open("extracted_data.json", "r") as json_file:
    extracted_data = json.load(json_file)
    if "skills" in extracted_data:
        user_skills = extracted_data["skills"]
        print(user_skills)

@app.route('/recommend_skills', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    job_description = data.get("job_description", "")
    
    if job_description:
        top_missing_skills = recommend_skills(job_description, user_skills)
        return jsonify(top_missing_skills)
    else:
        return jsonify({"message": "No job description provided."})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)