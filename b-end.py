from flask import Flask, request, jsonify
import whisper
from flask_cors import CORS
from dotenv import load_dotenv
import os


app = Flask(__name__)
cors_origin = os.getenv("CORS_ORIGIN","http://localhost:5173")  # Default to localhost if not set
CORS(app, origins=[cors_origin]) # Allow your frontend origin

# Load the Whisper model
model = whisper.load_model("base")

# Directory to save uploaded audio files
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create directory if it doesn't exist

@app.route('/')
def golu():
    return "Hello, World!"

@app.route('/golu')
def hello_world():
    return "Hello, Golu!"

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Save the incoming audio file locally in the uploads folder
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        print("path is :  " , file_path )
        
        # Perform transcription using Whisper on the saved file directly
        result = model.transcribe(file_path)

        # Return the transcription result as a JSON response
        response = jsonify({"transcription": result['text'], "file_saved": file_path})
        
        # Delete the recorded audio file
        os.remove(file_path)

        return response

    except Exception as e:
        # Print the error for debugging and return it as a JSON response
        print(f"Error found: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
