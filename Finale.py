import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import os
import time
import requests
from playsound import playsound
import re

# Dictionary mapping language codes to their names
language_names = {
    "en": "English",
    "bn": "Bengali",
    "gu": "Gujarati",
    "hi": "Hindi",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ma": "Punjabi",
    "sd": "Sindhi",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu"
}

def translate_text():
    text = input_text.get("1.0", "end-1c").strip()
    source_lang = source_lang_var.get()
    target_langs = [lang for lang, var in target_lang_vars.items() if var.get()]

    if not text:
        output_text.insert(tk.END, "Please enter text to translate.\n")
        return

    for target_lang in target_langs:
        lang_name = language_names.get(target_lang, "Unknown")

        # New URL and payload for the updated API
        url = "https://aibit-translator.p.rapidapi.com/api/v1/translator/html"
        payload = {
            "from": source_lang,
            "to": target_lang,
            "html": f"<p>{text}</p>"
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "82aa2b1fbbmsh4ef73325297a2f5p1bea3bjsnba30f3e7d41a",  # Replace with your actual API key
            "x-aibit-key": "5cf048c0-13ba-11ee-a37b-d799f0284f13"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            print("Response Status Code:", response.status_code)  # Debugging line
            print("Response Content:", response.content)          # Debugging line

            if response.status_code == 200:
                translation_data = response.json()
                translated_html = translation_data.get("trans")
                
                # Clean the HTML tags using a regular expression
                clean_text = re.sub(r'<[^>]+>', '', translated_html)
                
                if clean_text:
                    output_text.insert(tk.END, f"{lang_name}: {clean_text}\n")
                else:
                    output_text.insert(tk.END, f"Translation not available for {lang_name}\n")
            else:
                output_text.insert(tk.END, f"Error: Failed to translate to {lang_name}. Status Code: {response.status_code}\n")
        except requests.RequestException as e:
            output_text.insert(tk.END, f"Error: {str(e)}\n")

def text_to_voice():
    translated_texts = output_text.get("1.0", tk.END).strip()
    if translated_texts:
        tts = gTTS(text=translated_texts, lang='en')
        tts.save("output_voice.mp3")
        playsound("output_voice.mp3")
        os.remove("output_voice.mp3")
    else:
        output_text.insert(tk.END, "No valid translated text available for speech synthesis\n")

def reset_text():
    input_text.delete("1.0", "end")
    output_text.delete("1.0", "end")

def execute_action():
    action = action_var.get()
    if action == "Timed":
        current_time = time.strftime("%H:%M:%S")
        target_time = f"{hour_var.get()}:{minute_var.get()}:{second_var.get()}"

        current_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(current_time.split(":"))))
        target_time_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(target_time.split(":"))))

        time_remaining_seconds = (target_time_seconds - current_time_seconds) % (24 * 3600)
        time.sleep(time_remaining_seconds)

        translate_text()
        text_to_voice()
    elif action == "Delayed":
        delay = int(hour_var.get()) * 3600 + int(minute_var.get()) * 60 + int(second_var.get())
        time.sleep(delay)
        translate_text()
        text_to_voice()
    else:
        translate_text()
        text_to_voice()

def end_program():
    root.destroy()

root = tk.Tk()
root.title("Translation App")

# Input Frame
input_frame = ttk.Frame(root)
input_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

input_label = ttk.Label(input_frame, text="Enter text to translate:")
input_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

input_text = tk.Text(input_frame, height=5)
input_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)

# Language Selection
language_frame = ttk.Frame(input_frame)
language_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

source_lang_label = ttk.Label(language_frame, text="Source Language:")
source_lang_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

source_lang_var = tk.StringVar(value="en")
source_lang_dropdown = ttk.Combobox(language_frame, textvariable=source_lang_var, values=list(language_names.keys()))
source_lang_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

target_lang_label = ttk.Label(language_frame, text="Target Language(s):")
target_lang_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

target_lang_vars = {}
target_langs = list(language_names.keys())
for i, lang in enumerate(target_langs):
    var = tk.BooleanVar(value=False)
    target_lang_vars[lang] = var
    ttk.Checkbutton(language_frame, text=language_names[lang], variable=var).grid(row=1, column=i+1, padx=5, pady=5, sticky=tk.W)

# Action Frame
action_frame = ttk.Frame(root)
action_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

action_var = tk.StringVar(value="None")
action_label = ttk.Label(action_frame, text="Select Action:")
action_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

action_radios = [
    ("Timed", "Timed"),
    ("Delayed", "Delayed"),
    ("None", "None")
]

for i, (text, val) in enumerate(action_radios):
    ttk.Radiobutton(action_frame, text=text, variable=action_var, value=val).grid(row=0, column=i+1, padx=5, pady=5, sticky=tk.W)

hour_var = tk.StringVar(value="00")
hour_label = ttk.Label(action_frame, text="Hour:")
hour_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

hour_entry = ttk.Entry(action_frame, textvariable=hour_var, width=5)
hour_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

minute_var = tk.StringVar(value="00")
minute_label = ttk.Label(action_frame, text="Minute:")
minute_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

minute_entry = ttk.Entry(action_frame, textvariable=minute_var, width=5)
minute_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

second_var = tk.StringVar(value="00")
second_label = ttk.Label(action_frame, text="Second:")
second_label.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)

second_entry = ttk.Entry(action_frame, textvariable=second_var, width=5)
second_entry.grid(row=1, column=5, padx=5, pady=5, sticky=tk.W)

# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

translate_button = ttk.Button(button_frame, text="Translate", command=execute_action)
translate_button.grid(row=0, column=0, padx=5, pady=5)

reset_button = ttk.Button(button_frame, text="Reset", command=reset_text)
reset_button.grid(row=0, column=1, padx=5, pady=5)

end_button = ttk.Button(button_frame, text="End Program", command=end_program)
end_button.grid(row=0, column=2, padx=5, pady=5)

# Output Frame
output_frame = ttk.Frame(root)
output_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

output_label = ttk.Label(output_frame, text="Translated Text:")
output_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

output_text = tk.Text(output_frame, height=5)
output_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)

root.mainloop()
