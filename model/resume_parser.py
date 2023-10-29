from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

def parse_resume(resume_file):
    # Replace 'Your-Authorization-Token' with your actual authorization token
    headers = {'Authorization': '07accf5d-3a5b-426b-b9a4-6cb211e75a5d'}

    # Use requests to send the resume for parsing
    response = requests.post(
        url="https://www.docsaar.com/api/chatgpt_resume_parsing",
        headers=headers,
        files={'chatgpt_resume': resume_file}
    )

    if response.status_code == 200:
        data = response.json()

        skills = extract_skills(data)
        if skills:
            return skills

    return None

def extract_skills(data):
    if 'output' in data:
        output_data = data['output']
        skills = output_data.get("skills", [])
        return skills
    return None

@app.route('/parse_resume', methods=['POST'])
def parse_resume_endpoint():
    resume_file = request.files['resume']

    if resume_file:
        skills = parse_resume(resume_file)
        print(skills)
        if skills:
            extracted_data = {
                "skills": skills,
            }
            extracted_data_file_name = 'extracted_data.json'
            with open(extracted_data_file_name, 'w') as json_file:
                json.dump(extracted_data, json_file, indent=4)
            return jsonify({"message": "Resume analysis complete. Extracted data saved."})
        else:
            return jsonify({"error": "No skills data found in the response."})
    else:
        return jsonify({"error": "No resume file uploaded."})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
