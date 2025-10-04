import speech_recognition as sr
import pygame
import threading

trigger_words = [
    "help", "stop", "no", "danger", "please", "don't", "wait",
    "leave me", "someone", "rescue", "attack", "harassment",
    "abuse", "leave", "run", "get away", "assault", "stranger",
    "dangerous", "police", "emergency", "kidnap", "save me",
    "bachao", "madad", "madad karo", "mujhe bachao", "bachaiye", 
    "bacha lo","naaku help", "naaku sahayam cheyyandi", 
    "nannu baachandi", "sahayam", "sahaya", "nanna rakshisi", 
    "help madi", "dayaviṭṭu sahaya maadi"
]

help_messages = ["help1.mp3", "help2.mp3", "help3.mp3"]
siren_sound = "siren.mp3"

pygame.mixer.init()

def play_audio(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.delay(5)  # non-blocking small wait

def play_alert_sequence():
    def run_sequence():
        for _ in range(2):
            for msg in help_messages:
                play_audio(msg)
        play_audio(siren_sound)
    threading.Thread(target=run_sequence, daemon=True).start()

# Optional manual trigger
def manual_trigger():
    while True:
        input()
        play_alert_sequence()

threading.Thread(target=manual_trigger, daemon=True).start()

recognizer = sr.Recognizer()
mic = sr.Microphone()

while True:
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
            try:
                text = recognizer.recognize_google(audio).lower()
                if any(word in text for word in trigger_words):
                    play_alert_sequence()
            except:
                pass
    except:
        pass
