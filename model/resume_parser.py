from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/parse_resume', methods=['POST'])
def parse_resume():
    resume_file = request.files['resume']
    # Process and analyze the resume here
    # You can call your resume parsing code
    extracted_data = {
        "skills": ["Python", "Machine Learning", "Data Analysis"],  # Modify this based on your response structure
    }
    # Save the extracted data as extracted_data.json
    extracted_data_file_name = 'extracted_data.json'
    with open(extracted_data_file_name, 'w') as json_file:
        json.dump(extracted_data, json_file, indent=4)
    return jsonify({"message": "Resume analysis complete. Extracted data saved."})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
