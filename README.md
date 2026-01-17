# 🎙️ AI Voice Generator

A modern, full-stack Text-to-Speech (TTS) application built with **Flask** and **Google Text-to-Speech (gTTS)**. This application allows users to convert text into audio in multiple languages instantly without page reloads, featuring automatic server cleanup and concurrency handling.

## 🚀 Key Features

* **Asynchronous Generation:** Uses AJAX/Fetch API to generate audio in the background without reloading the page.
* **Smart Concurrency:** Implements `uuid` for unique filenames, ensuring multiple users can generate audio simultaneously without overwriting each other's files.
* **Auto-Cleanup System:** Includes a background thread that automatically monitors and deletes audio files older than 10 minutes to manage server storage efficiently.
* **Modern UI:** A clean, glass-morphism inspired interface with real-time character counting and loading states.
* **Multi-Language Support:** Supports English, Hindi, French, German, and Spanish.

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask, Threading (for background tasks)
* **Audio Processing:** gTTS (Google Text-to-Speech)
* **Frontend:** HTML5, CSS3 (Modern Flexbox), JavaScript (Async/Await)

## 📂 Project Structure

```text
AI_Audio_Generation/
├── app.py              # Main Flask application & background cleanup logic
├── requirements.txt    # Project dependencies
├── templates/
│   └── index.html      # Frontend user interface
├── static/
│   ├── style.css       # Custom styling
│   └── script.js       # Client-side logic (AJAX calls)
└── audio/              # Temporary storage for generated MP3s
