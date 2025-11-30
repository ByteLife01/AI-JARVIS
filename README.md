Markdown# J.A.R.V.I.S. Mark 15 (AI Assistant)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![OpenAI](https://img.shields.io/badge/AI-GPT--4o-green?style=for-the-badge&logo=openai)
![Status](https://img.shields.io/badge/Status-Operational-cyan?style=for-the-badge)

A fully functional, voice-activated AI assistant inspired by Iron Man.
Built with Python, this assistant features a **Holographic Arc Reactor GUI**, **Computer Vision**, **System Automation**, and **Real-time Internet Intelligence**.

## 🚀 Features

### 🧠 Core Intelligence
* **GPT-4o Integration:** Chat naturally, ask complex questions, and get intelligent responses.
* **Offline Voice:** Fast, low-latency speech recognition and text-to-speech.
* **Context Awareness:** Remembers previous conversations and knows the current date/time.

### 👁️ Computer Vision
* **Object Recognition:** Show objects to your webcam and ask *"What is this?"*
* **Image Analysis:** Uses OpenAI Vision to describe the real world.

### 💻 System Control (The "Hands")
* **App Automation:** Open apps like Notepad, Calculator, or games (Minecraft/Roblox) via voice.
* **Hardware Control:** Adjust **Volume** and **Screen Brightness**.
* **System Diagnostics:** Check **Battery %** and **CPU Usage**.
* **Screenshot:** Instantly save a capture of your screen.

### 🌐 Internet & Knowledge
* **Live Weather:** Check temperature and conditions for any city.
* **Stock Market:** Get real-time stock prices (e.g., *"Stock price of Tesla"*).
* **Wikipedia:** Read summaries of historical figures or events.
* **YouTube DJ:** Automatically find and play videos.
* **Google Search:** Open browser results instantly.

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Jarvis-Mark-15.git](https://github.com/YOUR_USERNAME/Jarvis-Mark-15.git)
cd Jarvis-Mark-15
2. Install DependenciesYou will need Python installed. Run this command to install the required libraries:Bashpip install customtkinter openai pyttsx3 SpeechRecognition pyaudio opencv-python duckduckgo-search pywhatkit psutil wikipedia yfinance pyautogui screen_brightness_control requests
🔑 ConfigurationTo enable the AI Brain, you must add your API Key.Open main.py in your code editor.Find Line 24:PythonMY_API_KEY = "PASTE_YOUR_OPENAI_KEY_HERE"
Replace the placeholder with your actual key starting with sk-....🎮 Adding Custom AppsYou can teach Jarvis to open your favorite games or software.Look for the APPS dictionary near the top of main.py:PythonAPPS = {
    "minecraft": r"C:\XboxGames\Minecraft Launcher\Content\Minecraft.exe",
    "discord": r"C:\Users\YourName\AppData\Local\Discord\Update.exe",
    # Add your own apps here!
}
🤖 UsageRun the assistant:Bashpython main.py
🗣️ Command ListCategoryCommand ExampleActionVision"Look at this"Activates camera & analyzes object.Media"Play Believer"Plays video on YouTube.System"Check battery"Reports battery & CPU health.Control"Volume up"Increases system volume.Control"Brightness to 50"Dims the screen.Web"Wiki Elon Musk"Reads Wikipedia summary.Web"Weather in London"Checks live weather.Web"Stock price of Apple"Checks live stock market.Tools"Take a screenshot"Saves screen image to folder.Tools"Take a note"Saves text to jarvis_notes.txt.Apps"Open Calculator"Launches the application.⚠️ Privacy NoteThis assistant uses your Microphone and Webcam. All data is processed locally or sent securely to OpenAI via your personal API key. No data is stored on external servers by this software.📜 LicenseThis project is open-source. Feel free to modify, upgrade, and build your own Mark 16!Created by Mohammed Al-Radhan
