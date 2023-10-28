import requests
import json

files = {'chatgpt_resume': open("./Sairaaj_Surve_Resume.pdf", 'rb')}
headers = {'Authorization': '310991a8-07d7-496f-aaec-c3c6a92cd0e6'}
response = requests.request(
    method='POST',
    headers=headers,
    url="https://www.docsaar.com/api/chatgpt_resume_parsing",
    files=files
)

if response.status_code == 200:
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

    print(f"Extracted data has been saved to '{extracted_data_file_name}'")
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
