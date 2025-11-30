import customtkinter as ctk
import threading
import speech_recognition as sr
from openai import OpenAI
import pyttsx3
import datetime
import webbrowser
import os
import subprocess
import math
import cv2
import base64
import time
from duckduckgo_search import DDGS
import pywhatkit 
import psutil
import wikipedia               
import yfinance as yf          
import pyautogui               
import screen_brightness_control as sbc 
import requests                

# ==========================================
# 1. USER CONFIGURATION (EDIT THIS!)
# ==========================================
# ⚠️ PASTE YOUR OPENAI API KEY HERE ⚠️
MY_API_KEY = "sk-" 

# A. WEBSITES (Voice Trigger: "Open [Name]")
WEBSITES = {
    "chatgpt": "https://chat.openai.com",
    "gmail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "netflix": "https://www.netflix.com",
    "twitter": "https://twitter.com"
}

# B. APPS (Voice Trigger: "Open [Name]")
# To add a new app, find its .exe file, hold Shift + Right Click, "Copy as path".
# Paste it below with an 'r' in front: r"C:\Path\To\Game.exe"
APPS = {
    "notepad": "notepad",
    "calculator": "calc",
    "cmd": "cmd",
    "settings": "start ms-settings:",
    
    # EXAMPLES (Remove # to use):
    # "minecraft": r"C:\XboxGames\Minecraft Launcher\Content\Minecraft.exe",
    # "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    # "discord": r"C:\Users\YOUR_USER\AppData\Local\Discord\Update.exe",
    # "spotify": r"C:\Users\YOUR_USER\AppData\Roaming\Spotify\Spotify.exe"
}

# ==========================================
# 2. SYSTEM CONFIG
# ==========================================
client = OpenAI(api_key=MY_API_KEY)

ARC_NEON  = "#00F0FF" 
ARC_DARK  = "#004859" 
ARC_BLACK = "#050505" 
ARC_WHITE = "#FFFFFF"

# ==========================================
# 3. THE BACKEND
# ==========================================
class JarvisBackend:
    def __init__(self, gui_app):
        self.gui = gui_app
        today_date = datetime.datetime.now().strftime("%B %d, %Y")
        self.conversation_history = [
            {"role": "system", "content": f"You are J.A.R.V.I.S. Today is {today_date}. Answer in 1 sentence."}
        ]
        self.recognizer = sr.Recognizer()
        
    def speak(self, text):
        self.gui.update_status(f"> {text}")
        print(f"Jarvis: {text}")
        try:
            engine = pyttsx3.init('sapi5')
            engine.setProperty('rate', 190)
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except:
            pass

    # --- UTILITY TOOLS ---
    def get_weather(self, city):
        self.speak(f"Checking weather for {city}...")
        try:
            url = f"https://wttr.in/{city}?format=3"
            response = requests.get(url)
            self.speak(f"Report: {response.text}")
        except:
            self.speak("Weather systems offline.")

    def get_wikipedia(self, topic):
        self.speak(f"Searching Wikipedia for {topic}...")
        try:
            result = wikipedia.summary(topic, sentences=2)
            self.speak(result)
        except:
            self.speak("No wikipedia entry found.")

    def get_stock(self, ticker):
        self.speak(f"Checking stock price for {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")['Close'].iloc[-1]
            self.speak(f"The price is {round(price, 2)} dollars.")
        except:
            self.speak("Stock data unavailable.")

    def take_screenshot(self):
        self.speak("Taking screenshot.")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        pyautogui.screenshot(filename)
        self.speak(f"Saved as {filename}")

    def take_note(self, text):
        self.speak("Saving note.")
        with open("jarvis_notes.txt", "a") as f:
            timestamp = datetime.datetime.now().strftime("%H:%M")
            f.write(f"[{timestamp}] {text}\n")
        self.speak("Note saved to file.")

    def control_brightness(self, level):
        self.speak(f"Setting brightness to {level} percent.")
        try:
            sbc.set_brightness(int(level))
        except:
            self.speak("Display control failed.")

    def check_system(self):
        battery = psutil.sensors_battery()
        cpu = psutil.cpu_percent()
        msg = f"CPU at {cpu}%."
        if battery:
            msg += f" Battery at {battery.percent}%."
        self.speak(msg)

    def play_youtube(self, video):
        self.speak(f"Playing {video}...")
        pywhatkit.playonyt(video)

    def google_search(self, query):
        self.speak(f"Opening Google for {query}...")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    def see(self):
        self.speak("Accessing visual sensors...")
        cam = cv2.VideoCapture(0)
        self.speak("Targeting...")
        for i in range(30):
            ret, frame = cam.read()
            if not ret: break
            cv2.imshow("JARVIS TARGETING", frame)
            cv2.waitKey(50) 
        ret, frame = cam.read()
        if ret:
            cv2.imwrite("vision.jpg", frame)
        cam.release()
        cv2.destroyAllWindows() 
        if ret:
            with open("vision.jpg", "rb") as img_file:
                base64_image = base64.b64encode(img_file.read()).decode('utf-8')
            self.speak("Analyzing...")
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": [
                            {"type": "text", "text": "Describe this image."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]}
                    ]
                )
                self.speak(response.choices[0].message.content)
            except:
                self.speak("Visual error.")
        else:
            self.speak("Camera failed.")

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=4) 
                command = self.recognizer.recognize_google(audio)
                return command.lower()
            except:
                return ""

    def run_cycle(self):
        self.speak("Mark 15 Online. All Systems Ready.")
        while True:
            self.gui.set_ai_status("listening")
            command = self.listen()
            if command:
                self.gui.set_ai_status("processing")
                self.process_command(command)
            else:
                self.gui.set_ai_status("idle")

    # --- THE COMMAND CENTER ---
    def process_command(self, command):
        # 1. SYSTEM CONTROL
        if "stop" in command or "exit" in command:
            self.speak("Powering down.")
            os._exit(0)
            
        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"Time: {now}")

        elif "system" in command or "battery" in command:
            self.check_system()
            
        elif "screenshot" in command:
            self.take_screenshot()
            
        elif "brightness" in command:
            try:
                level = [int(s) for s in command.split() if s.isdigit()][0]
                self.control_brightness(level)
            except:
                self.speak("Please say a number for brightness.")

        elif "volume up" in command:
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            self.speak("Volume increased.")

        elif "volume down" in command:
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            self.speak("Volume decreased.")

        # 2. ONLINE KNOWLEDGE
        elif "wiki" in command or "wikipedia" in command:
            topic = command.replace("wiki", "").replace("wikipedia", "").strip()
            self.get_wikipedia(topic)

        elif "weather" in command:
            if "in" in command:
                city = command.split("in")[-1].strip()
                self.get_weather(city)
            else:
                self.get_weather("New York")

        elif "stock" in command:
            self.speak("Finding ticker...")
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": f"What is the stock ticker symbol for {command}? Reply ONLY with the symbol (e.g. AAPL)."}]
                )
                ticker = response.choices[0].message.content.strip()
                self.get_stock(ticker)
            except:
                self.speak("Could not find that stock.")

        # 3. MEDIA & VISION
        elif "play" in command:
            song = command.replace("play", "").strip()
            self.play_youtube(song)

        elif "see" in command or "look" in command:
            self.see()

        elif "google" in command:
            topic = command.replace("google", "").replace("search", "").strip()
            self.google_search(topic)

        # 4. PRODUCTIVITY & APPS
        elif "note" in command:
            note_text = command.replace("take a note", "").replace("note", "").strip()
            self.take_note(note_text)

        elif "open" in command:
            found = False
            # Check Websites
            for site in WEBSITES:
                if site in command:
                    webbrowser.open(WEBSITES[site])
                    self.speak(f"Opening {site}...")
                    found = True
                    break
            # Check Apps
            if not found:
                for app in APPS:
                    if app in command:
                        if ".exe" not in APPS[app] and "\\" not in APPS[app]: 
                            os.system(APPS[app])
                        else: 
                            subprocess.Popen(APPS[app])
                        self.speak(f"Opening {app}...")
                        found = True
                        break
            if not found: self.speak("I don't have that app registered.")
            
        # 5. GENERAL AI
        else:
            self.conversation_history.append({"role": "user", "content": command})
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini", messages=self.conversation_history
                )
                reply = response.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": reply})
                self.speak(reply)
            except:
                self.speak("Server unavailable.")

# ==========================================
# 4. THE GUI (Mark 15)
# ==========================================
class JarvisGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("STARK INDUSTRIES | MARK 15")
        self.geometry("500x650")
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=ARC_BLACK)
        
        self.canvas = ctk.CTkCanvas(self, width=400, height=400, bg=ARC_BLACK, highlightthickness=0)
        self.canvas.pack(pady=40)
        
        self.label_status = ctk.CTkLabel(self, text="SYSTEM INITIALIZED", font=("Consolas", 16), text_color=ARC_NEON)
        self.label_status.pack(pady=10)
        
        self.footer = ctk.CTkLabel(self, text="STARK SYSTEM MODEL 15 // MASTER CONTROL", font=("Arial", 10), text_color="gray")
        self.footer.pack(side="bottom", pady=10)
        
        self.rotation = 0; self.pulse = 0; self.pulse_dir = 1; self.ai_status = "idle" 
        
        self.backend = JarvisBackend(self)
        self.thread = threading.Thread(target=self.backend.run_cycle)
        self.thread.daemon = True
        self.thread.start()
        
        self.animate()

    def update_status(self, text): 
        self.label_status.configure(text=text.upper())

    def set_ai_status(self, status): 
        self.ai_status = status

    def draw_reactor(self):
        self.canvas.delete("all"); cx, cy = 200, 200 
        
        if self.ai_status == "listening": core_size = 30 + (self.pulse * 2); color = ARC_WHITE
        elif self.ai_status == "processing": core_size = 30; color = "#FF3333" 
        else: core_size = 30 + self.pulse; color = ARC_NEON

        self.canvas.create_oval(cx-core_size, cy-core_size, cx+core_size, cy+core_size, fill=color, outline=color)
        self.canvas.create_oval(cx-60, cy-60, cx+60, cy+60, outline=ARC_DARK, width=2)
        
        radius = 120; num_ticks = 12
        for i in range(num_ticks):
            angle_deg = (i * (360/num_ticks)) + self.rotation
            angle_rad = math.radians(angle_deg)
            x1 = cx + (radius * math.cos(angle_rad)); y1 = cy + (radius * math.sin(angle_rad))
            x2 = cx + ((radius + 20) * math.cos(angle_rad)); y2 = cy + ((radius + 20) * math.sin(angle_rad))
            self.canvas.create_line(x1, y1, x2, y2, fill=ARC_NEON, width=5)
            
        self.canvas.create_oval(cx-135, cy-135, cx+135, cy+135, outline=ARC_DARK, width=1)

    def animate(self):
        if self.ai_status == "processing": self.rotation += 10 
        else: self.rotation += 1 
            
        if self.pulse_dir == 1:
            self.pulse += 0.5
            if self.pulse > 5: self.pulse_dir = -1
        else:
            self.pulse -= 0.5
            if self.pulse < 0: self.pulse_dir = 1
                
        self.draw_reactor()
        self.after(30, self.animate)

if __name__ == "__main__":
    app = JarvisGUI()
    app.mainloop()