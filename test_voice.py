import pyttsx3

print("Testing voice drivers...")

# 1. Force the Windows Driver (sapi5)
try:
    engine = pyttsx3.init('sapi5')
    
    # 2. Set properties
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0) # Max volume

    # 3. Speak
    print("Speaking now...")
    engine.say("Testing system audio. Can you hear me?")
    engine.runAndWait()
    print("Finished speaking.")

except Exception as e:
    print(f"Error found: {e}")