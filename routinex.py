import pyttsx3
import speech_recognition as sr
import schedule
import time
import webbrowser
import pywhatkit
from datetime import datetime
import sys

# ================== USER ==================
name = input("Enter your name: ")

# ================== SPEAK (FIXED) ==================
def speak(text):
    try:
        engine = pyttsx3.init()   # 🔥 new engine every time (main fix)

        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)

        engine.setProperty('rate', 155)
        engine.setProperty('volume', 1.0)

        print("Routine X:", text)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("Voice Error:", e)

# TEST VOICE
speak("Voice system is ready")

# ================== LISTEN ==================
def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)

        cmd = r.recognize_google(audio)
        print("You:", cmd)
        return cmd.lower()

    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print("Mic Error:", e)
        return ""

# ================== REMINDER ==================
def remind(task):
    speak(f"{name}, it's time for {task}")

# ================== TIME INPUT ==================
def get_time(prompt):
    while True:
        t = input(prompt)
        try:
            datetime.strptime(t, "%H:%M")
            return t
        except:
            print("Use format HH:MM (24 hour)")

# ================== TIMETABLE ==================
tasks = ["Wake up", "Breakfast", "College", "Lunch", "Study", "Gym", "Dinner", "Sleep"]
timetable = []

print("\n--- Setup Your Schedule ---")

for task in tasks:
    choice = input(f"Add {task}? (yes/no): ").lower()
    if choice == "yes":
        t = get_time(f"Enter time for {task}: ")
        timetable.append((t, task))

# ================== SCHEDULE ==================
speak("Setting your schedule")

for t, task in timetable:
    schedule.every().day.at(t).do(remind, task)
    speak(f"{task} scheduled at {t}")

speak("Your schedule is ready")

# ================== BRAIN ==================
def brain(cmd):

    if "hello" in cmd or "hi" in cmd:
        speak(f"Hello {name}, I am ready")

    elif "time" in cmd:
        speak(datetime.now().strftime("The time is %H:%M"))

    elif "open youtube" in cmd:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open google" in cmd:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open instagram" in cmd:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")

    elif "play" in cmd:
        song = cmd.replace("play", "").strip()
        if song:
            speak(f"Playing {song}")
            pywhatkit.playonyt(song)
        else:
            speak("Say song name")

    elif "exit" in cmd or "stop" in cmd:
        speak("Goodbye")
        sys.exit()

    elif cmd != "":
        speak("I did not understand")

# ================== START ==================
speak(f"Hello {name}, Routine X is now active")

# ================== MAIN LOOP ==================
while True:
    schedule.run_pending()

    command = listen()
    if command:
        brain(command)

    time.sleep(0.5)   # 🔥 smoother loop