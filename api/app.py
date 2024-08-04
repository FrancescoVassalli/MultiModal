import json
import os
from flask import Flask
from flask_cors import CORS
from flask import request
from dotenv import load_dotenv
from multi_snow.groq_call import run_conversation

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def hello_world():
    return json.dumps({"message": "Hello, World!"})


@app.route("/chat-input", methods=["POST"])
def chat_input():
    # Get JSON data from the request
    data = request.get_json()

    # Execute the Python package function using the JSON string
    result = run_conversation(data['message'])

    print(f"Flask results: {result}")

    return json.dumps({"message": "Success", "result": result})




if __name__ == "__main__":
    # Check if the FLASK_DEBUG environment variable is set to 'True'
    debug_mode = os.environ.get("FLASK_DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=8080, debug=debug_mode)
