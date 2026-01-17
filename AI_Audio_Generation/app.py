from flask import Flask, render_template, request, send_from_directory, jsonify
from gtts import gTTS  # type: ignore
import os
import uuid
import time
import threading
from typing import Any

app = Flask(__name__)

# Configuration
AUDIO_FOLDER = "audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Cleanup Settings (in seconds)
FILE_LIFETIME = 600  # Delete files older than 10 minutes
CLEANUP_INTERVAL = 600  # Run the cleanup check every 10 minutes

def cleanup_old_files():
    """
    Background task to delete old audio files to save space.
    """
    while True:
        try:
            now = time.time()
            # Iterate over all files in the audio directory
            for filename in os.listdir(AUDIO_FOLDER):
                file_path = os.path.join(AUDIO_FOLDER, filename)
                
                # Check if it's a file (not a directory)
                if os.path.isfile(file_path):
                    file_creation_time = os.path.getmtime(file_path)
                    
                    # If file is older than FILE_LIFETIME, delete it
                    if now - file_creation_time > FILE_LIFETIME:
                        os.remove(file_path)
                        print(f"Deleted old file: {filename}")
                        
        except Exception as e:
            print(f"Error during cleanup: {e}")
        
        # Wait for the next cleanup cycle
        time.sleep(CLEANUP_INTERVAL)

# Start the cleanup task in a background thread
# daemon=True ensures the thread dies when the main application stops
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

@app.route("/")
def index() -> str:
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts() -> Any:
    data = request.get_json()
    text = data.get("text")
    language = data.get("language")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(AUDIO_FOLDER, filename)

        # Generate Audio
        tts = gTTS(text=text, lang=language)
        tts.save(file_path)

        return jsonify({
            "success": True,
            "audio_url": f"/audio/{filename}",
            "filename": filename
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/audio/<filename>")
def serve_audio(filename: str) -> Any:
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)