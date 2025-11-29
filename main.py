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

# ==========================================
# 1. USER CONFIGURATION
# ==========================================
MY_API_KEY = "" 

# WEB & APP LISTS
WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "chatgpt": "https://chat.openai.com",
    "gmail": "https://mail.google.com"
}

APPS = {
    "notepad": "notepad",
    "calculator": "calc",
    "cmd": "cmd",
    # Add your own apps here: "name": r"C:\Path\To\App.exe"
}

# ==========================================
# 2. SYSTEM CONFIG
# ==========================================
client = OpenAI(api_key=MY_API_KEY)

# Theme: Arc Reactor Blue
ARC_NEON  = "#00F0FF" # Bright Cyan
ARC_DARK  = "#004859" # Darker Cyan
ARC_BLACK = "#050505" # Deep Black
ARC_WHITE = "#FFFFFF"

# ==========================================
# 3. THE BACKEND (Brain, Voice, Vision)
# ==========================================
class JarvisBackend:
    def __init__(self, gui_app):
        self.gui = gui_app
        self.conversation_history = [
            {"role": "system", "content": "You are J.A.R.V.I.S. Answer in 1 sentence."}
        ]
        self.recognizer = sr.Recognizer()
        
    def speak(self, text):
        self.gui.update_status(f"> {text}")
        print(f"Jarvis: {text}")
        try:
            # Re-init engine to prevent freezing
            engine = pyttsx3.init('sapi5')
            engine.setProperty('rate', 190)
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except:
            pass

    def open_website(self, site_name):
        if site_name in WEBSITES:
            self.speak(f"Accessing {site_name}...")
            webbrowser.open(WEBSITES[site_name])
            return True
        return False

    def open_app(self, app_name):
        if app_name in APPS:
            self.speak(f"Protocol: {app_name}...")
            try:
                if ".exe" not in APPS[app_name] and "\\" not in APPS[app_name]:
                    os.system(APPS[app_name])
                else:
                    subprocess.Popen(APPS[app_name])
                return True
            except:
                self.speak(f"Error launching {app_name}.")
        return False

    def search_web(self, query):
        self.speak(f"Searching database for {query}...")
        try:
            results = DDGS().text(query, max_results=1)
            if results:
                self.speak(f"Result: {results[0]['body']}")
            else:
                self.speak("No data found.")
        except:
            self.speak("Connection failure.")

    # --- THE VISION FUNCTION ---
    def see(self):
        self.speak("Accessing visual sensors...")
        
        # 1. Open Camera
        cam = cv2.VideoCapture(0)
        
        # 2. Show the user what Jarvis sees
        self.speak("Targeting...")
        for i in range(30): # Show feed for ~1.5 seconds
            ret, frame = cam.read()
            if not ret: break
            cv2.imshow("JARVIS TARGETING", frame)
            cv2.waitKey(50) 
            
        # 3. Capture the final frame
        ret, frame = cam.read()
        if ret:
            cv2.imwrite("vision.jpg", frame)
            
        # 4. Clean up
        cam.release()
        cv2.destroyAllWindows() 
        
        # 5. Send to OpenAI
        if ret:
            with open("vision.jpg", "rb") as img_file:
                base64_image = base64.b64encode(img_file.read()).decode('utf-8')
                
            self.speak("Analyzing structure...")
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user", 
                            "content": [
                                {"type": "text", "text": "Describe this image briefly."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }
                    ]
                )
                self.speak(response.choices[0].message.content)
            except:
                self.speak("Visual processing error.")
        else:
            self.speak("Camera malfunction.")

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
        self.speak("Mark 11 UI Loaded. Systems Online.")
        
        while True:
            self.gui.set_ai_status("listening")
            command = self.listen()
            
            if command:
                self.gui.set_ai_status("processing")
                self.process_command(command)
            else:
                self.gui.set_ai_status("idle")

    def process_command(self, command):
        if "stop" in command or "exit" in command:
            self.speak("Powering down.")
            os._exit(0)
            
        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"Time: {now}")
            
        # VISION COMMAND
        elif "see" in command or "look" in command or "what is this" in command:
            self.see()

        elif "open" in command:
            found = False
            for site in WEBSITES:
                if site in command:
                    self.open_website(site)
                    found = True
                    break
            if not found:
                for app in APPS:
                    if app in command:
                        self.open_app(app)
                        found = True
                        break
                        
        elif "search" in command:
            topic = command.replace("search for", "").strip()
            self.search_web(topic)
            
        else:
            self.ask_gpt(command)

    def ask_gpt(self, text):
        self.conversation_history.append({"role": "user", "content": text})
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
# 4. THE BEAUTIFUL GUI (MARK 11 FIXED)
# ==========================================
class JarvisGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("STARK INDUSTRIES | MARK 11")
        self.geometry("500x650")
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=ARC_BLACK)

        # Main Layout
        self.canvas = ctk.CTkCanvas(self, width=400, height=400, bg=ARC_BLACK, highlightthickness=0)
        self.canvas.pack(pady=40)

        # Text Labels
        self.label_status = ctk.CTkLabel(self, text="SYSTEM INITIALIZED", font=("Consolas", 16), text_color=ARC_NEON)
        self.label_status.pack(pady=10)

        # Decorative Footer
        self.footer = ctk.CTkLabel(self, text="STARK SYSTEM MODEL 11 // VER 4.0.2", font=("Arial", 10), text_color="gray")
        self.footer.pack(side="bottom", pady=10)

        # Animation Vars
        self.rotation = 0
        self.pulse = 0
        self.pulse_dir = 1
        
        # RENAMED VARIABLE TO FIX BUG
        self.ai_status = "idle" 

        # Start Backend
        self.backend = JarvisBackend(self)
        self.thread = threading.Thread(target=self.backend.run_cycle)
        self.thread.daemon = True 
        self.thread.start()

        # Start Loop
        self.animate()

    def update_status(self, text):
        self.label_status.configure(text=text.upper())

    def set_ai_status(self, status):
        self.ai_status = status

    def draw_reactor(self):
        self.canvas.delete("all") # Clear screen
        cx, cy = 200, 200 # Center point

        # 1. CORE GLOW (Pulsing)
        if self.ai_status == "listening":
            core_size = 30 + (self.pulse * 2) # Beat fast
            color = ARC_WHITE
        elif self.ai_status == "processing":
            core_size = 30
            color = "#FF3333" # Red when thinking
        else:
            core_size = 30 + self.pulse
            color = ARC_NEON

        # Draw Glow
        self.canvas.create_oval(cx-core_size, cy-core_size, cx+core_size, cy+core_size, fill=color, outline=color)

        # 2. INNER RING (Solid)
        self.canvas.create_oval(cx-60, cy-60, cx+60, cy+60, outline=ARC_DARK, width=2)
        
        # 3. OUTER SEGMENTED RING (Spinning)
        radius = 120
        num_ticks = 12
        
        for i in range(num_ticks):
            angle_deg = (i * (360/num_ticks)) + self.rotation
            angle_rad = math.radians(angle_deg)
            
            x1 = cx + (radius * math.cos(angle_rad))
            y1 = cy + (radius * math.sin(angle_rad))
            x2 = cx + ((radius + 20) * math.cos(angle_rad))
            y2 = cy + ((radius + 20) * math.sin(angle_rad))
            
            self.canvas.create_line(x1, y1, x2, y2, fill=ARC_NEON, width=5)

        # 4. DECORATIVE CIRCLES
        self.canvas.create_oval(cx-135, cy-135, cx+135, cy+135, outline=ARC_DARK, width=1)

    def animate(self):
        # Update Rotation
        if self.ai_status == "processing":
            self.rotation += 10 # Spin fast
        else:
            self.rotation += 1 # Spin slow

        # Update Pulse
        if self.pulse_dir == 1:
            self.pulse += 0.5
            if self.pulse > 5: self.pulse_dir = -1
        else:
            self.pulse -= 0.5
            if self.pulse < 0: self.pulse_dir = 1

        # Redraw
        self.draw_reactor()
        self.after(30, self.animate)

if __name__ == "__main__":
    app = JarvisGUI()
    app.mainloop()