from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/test-get', methods=['GET'])
def get_data():
    return jsonify({'message': 'Flask server'})

@app.route('/test-post', methods=['POST'])
def receive_data():
    data = request.get_json()
    print(data) # to check if data is properly recieved
    # we can process or store the received data here
    return jsonify({'message': 'Data received by Flask'})

if __name__ == "__main__":
    app.run(port=5000, debug=True)