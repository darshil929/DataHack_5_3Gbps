from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/parse_resume", methods=["POST"])
def parse_resume():
    if 'resume' not in request.files:
        return "No resume file provided", 400

    resume = request.files['resume']
    # Your resume parsing code here...

    # Example parsing code
    extracted_data = {}  # Replace this with your actual parsing logic

    # Save the extracted data to a JSON file
    with open('extracted_data.json', 'w') as json_file:
        json.dump(extracted_data, json_file, indent=4)

    return "Resume parsed and data saved successfully", 200

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
