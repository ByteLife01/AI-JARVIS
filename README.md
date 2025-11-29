# J.A.R.V.I.S. - AI Assistant (Python)

![Python](https://img.shields.io/badge/Python-3.12-blue) ![OpenAI](https://img.shields.io/badge/AI-OpenAI_GPT4o-green) ![Status](https://img.shields.io/badge/Status-Operational-cyan)

A fully functional, voice-activated AI assistant inspired by Iron Man's J.A.R.V.I.S.
Built with Python, this assistant features a futuristic **Holographic GUI**, **Computer Vision**, and **Real-time Web Search**.

[Insert a Screenshot of your GUI here]

## 🚀 Features

* **🎙️ Voice Interaction:** fast speech-to-text and text-to-speech engine (Offline/Local).
* **🧠 Super Intelligence:** Powered by OpenAI's **GPT-4o**, allowing it to answer complex questions, code, and chat naturally.
* **👁️ Computer Vision:** Can "see" through your webcam. Just say *"Jarvis, look at this"* and it will describe the object.
* **⚛️ Holographic Interface:** A beautiful, animated Arc Reactor GUI built with CustomTkinter.
* **🌐 Internet Access:** Can perform real-time Google/DuckDuckGo searches.
* **💻 System Control:** Can open apps (Calculator, Notepad, etc.) and websites (YouTube, Google) via voice command.

## 🛠️ Installation

1.  **Clone the repository** (or download the zip):
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Jarvis.git](https://github.com/YOUR_USERNAME/Jarvis.git)
    cd Jarvis
    ```

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration

To make J.A.R.V.I.S. work, you need an API Key.

1.  Open `main.py`.
2.  Find **Line 21**:
    ```python
    MY_API_KEY = "PASTE_YOUR_KEY_HERE"
    ```
3.  Replace the text with your actual OpenAI API Key (starts with `sk-...`).

### Adding Custom Apps
You can teach Jarvis to open your specific apps by editing the `APPS` list in `main.py`:

```python
APPS = {
    "discord": r"C:\Users\YourName\AppData\Local\Discord\Update.exe",
    "spotify": r"C:\Users\YourName\AppData\Roaming\Spotify\Spotify.exe"
}

Command,Action
"""Jarvis""",Wakes him up (if in sleep mode).
"""Look at this""",Activates camera to analyze objects.
"""Search for [topic]""",Searches the live internet.
"""Open [App/Website]""","Opens Google, YouTube, Notepad, etc."
"""Time""",Tells the current time.
"""Stop"" / ""Exit""",Shuts down the system.

Here is a professional README.md file for your project.You can create a file named README.md in your VS Code, paste this text inside, and save it. It will look beautiful when you upload it to GitHub.Markdown# J.A.R.V.I.S. - AI Assistant (Python)

![Python](https://img.shields.io/badge/Python-3.12-blue) ![OpenAI](https://img.shields.io/badge/AI-OpenAI_GPT4o-green) ![Status](https://img.shields.io/badge/Status-Operational-cyan)

A fully functional, voice-activated AI assistant inspired by Iron Man's J.A.R.V.I.S.
Built with Python, this assistant features a futuristic **Holographic GUI**, **Computer Vision**, and **Real-time Web Search**.

[Insert a Screenshot of your GUI here]

## 🚀 Features

* **🎙️ Voice Interaction:** fast speech-to-text and text-to-speech engine (Offline/Local).
* **🧠 Super Intelligence:** Powered by OpenAI's **GPT-4o**, allowing it to answer complex questions, code, and chat naturally.
* **👁️ Computer Vision:** Can "see" through your webcam. Just say *"Jarvis, look at this"* and it will describe the object.
* **⚛️ Holographic Interface:** A beautiful, animated Arc Reactor GUI built with CustomTkinter.
* **🌐 Internet Access:** Can perform real-time Google/DuckDuckGo searches.
* **💻 System Control:** Can open apps (Calculator, Notepad, etc.) and websites (YouTube, Google) via voice command.

## 🛠️ Installation

1.  **Clone the repository** (or download the zip):
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Jarvis.git](https://github.com/YOUR_USERNAME/Jarvis.git)
    cd Jarvis
    ```

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration

To make J.A.R.V.I.S. work, you need an API Key.

1.  Open `main.py`.
2.  Find **Line 21**:
    ```python
    MY_API_KEY = "PASTE_YOUR_KEY_HERE"
    ```
3.  Replace the text with your actual OpenAI API Key (starts with `sk-...`).

### Adding Custom Apps
You can teach Jarvis to open your specific apps by editing the `APPS` list in `main.py`:

```python
APPS = {
    "discord": r"C:\Users\YourName\AppData\Local\Discord\Update.exe",
    "spotify": r"C:\Users\YourName\AppData\Roaming\Spotify\Spotify.exe"
}
🤖 How to UseRun the main script:Bashpython main.py
Voice CommandsCommandAction"Jarvis"Wakes him up (if in sleep mode)."Look at this"Activates camera to analyze objects."Search for [topic]"Searches the live internet."Open [App/Website]"Opens Google, YouTube, Notepad, etc."Time"Tells the current time."Stop" / "Exit"Shuts down the system.📦 RequirementsPython 3.10 or newerA working MicrophoneA Webcam (for Vision features)OpenAI API Key📜 LicenseThis project is for educational purposes. Feel free to modify and upgrade it!Created by [Mohammed Al-Radhan]

