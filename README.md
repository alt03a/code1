🎙️ Real-Time Voice Translator App
A simple and elegant real-time voice translator app with a fullscreen GUI built using Python, Tkinter, gTTS, SpeechRecognition, and Google Translate API. It continuously listens to spoken language, translates it into the target language, and speaks the result aloud — ideal for real-time conversations and demonstrations like in the Indian Lok Sabha!

✨ Features
🎧 Real-time voice recognition using microphone input

🌍 Language translation using Google Translate (online)

🔊 Spoken output using gTTS (Google Text-to-Speech)

⏯️ Start, Pause, Resume, and Stop translation controls

🔁 Continuous listening and speaking loop

🖥️ Fullscreen dark-themed GUI with live text display

🧵 Multithreaded audio queue for non-blocking TTS playback

🗣️ Language selector for both source and target languages

📋 Supported Languages
English (en)

Hindi (hi)

Bengali (bn)

You can add more language support by modifying the LANGUAGES dictionary.

🛠️ Requirements
Python 3.7+

Required packages (install using pip):

bash
Copy
Edit
pip install gTTS pygame SpeechRecognition googletrans==4.0.0-rc1
Note: googletrans depends on internet access and may occasionally face rate limits.

🚀 How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/voice-translator-app.git
cd voice-translator-app
Run the app:

bash
Copy
Edit
python voice_translator.py
The app will open in fullscreen. Press Exit to close.

🧩 File Structure
bash
Copy
Edit
voice_translator.py      # Main application code
README.md                # Project documentation
📸 GUI Preview
Feature	Preview
Language Selection	✅ Drop-down menus (From, To)
Listening Indicator	🎙️ Animated label (pulses white/red)
Original & Translated Text	🗣️ + 📝 shown in large fonts
Controls	Start / Pause / Resume / Stop / Exit

⚠️ Known Limitations
Requires stable internet connection for both translation and TTS.

No offline mode (yet).

TTS delay may occur depending on network and speech length.

✅ To-Do (Future Scope)
 Add offline STT and TTS (e.g., Vosk + pyttsx3)

 Support more languages

 Add waveform animation for mic input

 Improve UI responsiveness and error handling

👨‍💻 Author
Sk Altab Hossen
Final-year B.Tech (IT) Student
Feel free to connect and contribute!

📄 License
This project is open-source and available under the MIT License.

