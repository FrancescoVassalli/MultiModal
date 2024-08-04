import json
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def hello_world():
    return json.dumps({"message": "Hello, World!"})

if __name__ == "__main__":
    # Check if the FLASK_DEBUG environment variable is set to 'True'
    debug_mode = os.environ.get("FLASK_DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=8080, debug=debug_mode)
