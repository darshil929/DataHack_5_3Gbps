import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import pickle  # Import the pickle module
import json

# Load the extracted skills from extracted_data.json
with open('extracted_data.json', 'r') as file:
    data = json.load(file)

# Load the spaCy model for NLP
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

if __name__ == '__main__':
    with open('job_recommendation_model.pkl', 'wb') as file:
        pickle.dump(recommend_skills, file)
