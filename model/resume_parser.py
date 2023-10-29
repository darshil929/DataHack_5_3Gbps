from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    # Check if a file is provided in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    uploaded_file = request.files['file']

    # Check if the file has a valid name
    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Define the API endpoint and headers
    api_url = "https://www.docsaar.com/api/chatgpt_resume_parsing"
    api_headers = {'Authorization': '310991a8-07d7-496f-aaec-c3c6a92cd0e6'}

    # Send the file to the parsing API
    try:
        files = {'chatgpt_resume': (uploaded_file.filename, uploaded_file)}
        response = requests.post(api_url, headers=api_headers, files=files)

        if response.status_code == 200:
            data = response.json()

            keywords = ["skills"]

            extracted_data = {}

            for key, value in data["output"].items():
                for keyword in keywords:
                    if keyword.lower() in key.lower():
                        extracted_data[keyword] = value

            # Save extracted data to a JSON file
            extracted_data_file_name = 'extracted_data.json'
            with open(extracted_data_file_name, 'w') as json_file:
                json.dump(extracted_data, json_file, indent=4)

            return jsonify({'message': f'Extracted data has been saved to {extracted_data_file_name}'})
        else:
            return jsonify({'error': f'Request failed with status code {response.status_code}: {response.text}'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
