from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# Directory to save uploaded resumes
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def analyze_resume(resume_file_path):
    print(resume_file_path)
    files = {'chatgpt_resume': open(resume_file_path, 'rb')}
    headers = {'Authorization': '49692155-5dc2-404a-92c8-b70279666c3f'}
    response = requests.post(
        url="https://www.docsaar.com/api/chatgpt_resume_parsing",
        headers=headers,
        files=files
    )

    if response.status_code == 200:
        try:
            data = response.json()
            keywords = ["skills"]
            extracted_data = {}

            for key, value in data["output"].items():
                for keyword in keywords:
                    if keyword.lower() in key.lower():
                        extracted_data[keyword] = value

            extracted_data_file_name = 'extracted_data.json'
            
            with open(extracted_data_file_name, 'w') as json_file:
                json.dump(extracted_data, json_file, indent=4)

            return {"message": f"Resume analysis complete. Extracted data saved to '{extracted_data_file_name}'"}
        except json.JSONDecodeError as e:
            return {"error": f"Failed to decode JSON response: {str(e)}"}
    else:
        return {"error": f"Resume analysis failed with status code {response.status_code}: {response.text}"}

@app.route('/parse_resume', methods=['POST'])
def parse_resume():
    resume_file = request.files['resume']
    
    if resume_file:
        # Save the uploaded resume to the uploads folder
        resume_path = os.path.join(UPLOAD_FOLDER, "uploaded_resume.pdf")
        resume_file.save(resume_path)

        # Analyze the resume
        data = analyze_resume(resume_path)

        if "error" in data:
            return jsonify(data)
        else:
            return jsonify(data)
    else:
        return jsonify({"error": "No resume file provided."})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
