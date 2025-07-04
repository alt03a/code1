import os
import threading
import time
import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import pygame
import queue
import speech_recognition as sr
from googletrans import Translator

# Flags
isTranslateOn = False
isPaused = False

# Translator and audio init
translator = Translator()
pygame.mixer.init()

LANGUAGES = {
    'english': 'en',
    'hindi': 'hi',
    'bengali': 'bn'
}

def get_language_code(name):
    return LANGUAGES.get(name.lower(), 'en')

tts_queue = queue.Queue()

def tts_worker():
    while True:
        item = tts_queue.get()
        if item is None:
            break
        text, lang_code = item
        try:
            filename = f"temp_{int(time.time()*1000)}.mp3"
            tts = gTTS(text=text, lang=lang_code)
            tts.save(filename)
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.05)
            os.remove(filename)
        except Exception as e:
            print("TTS Error:", e)
        tts_queue.task_done()

threading.Thread(target=tts_worker, daemon=True).start()

def update_text_display(original, translated):
    original_text_var.set("🗣 " + original)
    translated_text_var.set("📝 " + translated)

def translate_and_speak_continuous(src_lang, tgt_lang):
    global isTranslateOn, isPaused
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

    def loop():
        global isTranslateOn, isPaused
        while isTranslateOn:
            if isPaused:
                time.sleep(0.2)
                continue
            with mic as source:
                try:
                    status_label.config(text="🎙️ Listening...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = recognizer.recognize_google(audio, language=src_lang)
                    translated = translator.translate(text, src=src_lang, dest=tgt_lang)
                    update_text_display(text, translated.text)
                    tts_queue.put((translated.text, tgt_lang))
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print("Error:", e)

    threading.Thread(target=loop, daemon=True).start()

def start_translation():
    global isTranslateOn, isPaused
    if not isTranslateOn:
        isTranslateOn = True
        isPaused = False
        src_code = get_language_code(source_lang_var.get())
        tgt_code = get_language_code(target_lang_var.get())
        translate_and_speak_continuous(src_code, tgt_code)

def pause_translation():
    global isPaused
    isPaused = True
    status_label.config(text="⏸️ Paused")

def resume_translation():
    global isPaused
    isPaused = False
    status_label.config(text="🎙️ Listening...")

def stop_translation():
    global isTranslateOn
    isTranslateOn = False
    pygame.mixer.music.stop()
    original_text_var.set("")
    translated_text_var.set("")
    status_label.config(text="🛑 Stopped")

# GUI setup
root = tk.Tk()
root.title("Real-Time Voice Translator")
root.attributes('-fullscreen', True)  # Fullscreen
root.configure(bg="#121212")

# Styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 14), padding=10, relief="flat", background="#444", foreground="white")
style.map("TButton", background=[("active", "#666")])

# Top Panel
top_frame = tk.Frame(root, bg="#121212")
top_frame.pack(pady=20)

source_lang_var = tk.StringVar(value='English')
target_lang_var = tk.StringVar(value='Hindi')

ttk.Label(top_frame, text="From:", font=("Arial", 16), foreground="white", background="#121212").grid(row=0, column=0, padx=10)
source_dropdown = ttk.Combobox(top_frame, textvariable=source_lang_var, values=list(LANGUAGES.keys()), font=("Arial", 14), state="readonly", width=12)
source_dropdown.grid(row=0, column=1, padx=10)

ttk.Label(top_frame, text="To:", font=("Arial", 16), foreground="white", background="#121212").grid(row=0, column=2, padx=10)
target_dropdown = ttk.Combobox(top_frame, textvariable=target_lang_var, values=list(LANGUAGES.keys()), font=("Arial", 14), state="readonly", width=12)
target_dropdown.grid(row=0, column=3, padx=10)

# Status Label
status_label = tk.Label(root, text="🔴 Not Listening", font=("Arial", 16), fg="tomato", bg="#121212")
status_label.pack(pady=5)

# Text Display
original_text_var = tk.StringVar()
translated_text_var = tk.StringVar()

tk.Label(root, textvariable=original_text_var, font=("Arial", 18), fg="white", bg="#121212", wraplength=1000).pack(pady=10)
tk.Label(root, textvariable=translated_text_var, font=("Arial", 22, "bold"), fg="#00FF7F", bg="#121212", wraplength=1000).pack(pady=5)

# Button Panel
button_frame = tk.Frame(root, bg="#121212")
button_frame.pack(pady=20)

def make_button(text, command, color):
    return tk.Button(button_frame, text=text, command=command, font=("Arial", 16), bg=color, fg="white", width=15, bd=0, relief="ridge", activebackground="#333")

make_button("Start", start_translation, "#28a745").grid(row=0, column=0, padx=10, pady=5)
make_button("Pause", pause_translation, "#ffc107").grid(row=0, column=1, padx=10, pady=5)
make_button("Resume", resume_translation, "#17a2b8").grid(row=0, column=2, padx=10, pady=5)
make_button("Stop", stop_translation, "#dc3545").grid(row=0, column=3, padx=10, pady=5)
make_button("Exit", root.destroy, "#6c757d").grid(row=1, column=1, columnspan=2, pady=10)

# Pulsing effect on status label
def pulse():
    current = status_label.cget("fg")
    status_label.config(fg="white" if current == "tomato" else "tomato")
    root.after(600, pulse)

pulse()
root.mainloop()
