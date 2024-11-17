import boto3
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import pygame
import os
import time

pygame.mixer.init()

output_format = 'mp3'


def text_to_speech_aws(text, voice, speech_rate, output_format):
    polly_client = boto3.client('polly')

    output_file = f'speech_{int(time.time())}.{output_format}'

    try:
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice,
            Engine='standard',
            SpeechMarkTypes=[],
            LanguageCode='en-US'
        )

        if "AudioStream" in response:
            with open(output_file, "wb") as file:
                file.write(response['AudioStream'].read())
            messagebox.showinfo("Success", f"Audio content saved to {output_file}")

            play_audio(output_file)
        else:
            messagebox.showerror("Error", "Could not retrieve audio stream.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def play_audio(audio_file):
    pygame.mixer.music.stop()

    if os.path.exists(audio_file):
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        messagebox.showerror("Error", f"Audio file {audio_file} does not exist.")


def convert_text():
    text = text_entry.get("1.0", tk.END).strip()
    if text:
        selected_voice = voice_var.get()
        speech_rate = speed_scale.get()
        text_to_speech_aws(text, selected_voice, speech_rate, output_format)
    else:
        messagebox.showwarning("Input Error", "Please enter some text.")


def clear_text():
    text_entry.delete("1.0", tk.END)


def stop_audio():
    pygame.mixer.music.stop()


def save_text():
    text = text_entry.get("1.0", tk.END).strip()
    if text:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(text)
            messagebox.showinfo("Success", f"Text saved to {file_path}")
    else:
        messagebox.showwarning("Input Error", "Nothing to save.")


def load_text():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text_entry.delete("1.0", tk.END)
            text_entry.insert(tk.END, file.read())
    else:
        messagebox.showwarning("File Error", "No file selected.")


root = tk.Tk()
root.title("Enhanced Text-to-Speech with AWS Polly")
root.geometry("500x600")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=6, relief="flat", background="#007ACC")
style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
style.configure("TText", font=("Helvetica", 10))

voice_var = tk.StringVar(value="Joanna")
voice_options = ['Joanna', 'Matthew', 'Ivy', 'Salli', 'Kendra', 'Kimberly']
voice_label = ttk.Label(root, text="Select Voice:")
voice_label.pack(pady=5)
voice_menu = ttk.Combobox(root, textvariable=voice_var, values=voice_options, state="readonly")
voice_menu.pack(pady=5)

speed_label = ttk.Label(root, text="Speech Speed (1.0 is Normal):")
speed_label.pack(pady=5)
speed_scale = ttk.Scale(root, from_=0.5, to=2.0, length=300, value=1.0, orient=tk.HORIZONTAL)
speed_scale.pack(pady=5)

output_format_label = ttk.Label(root, text="Select Output Format:")
output_format_label.pack(pady=5)
format_var = tk.StringVar(value="mp3")
format_menu = ttk.Combobox(root, textvariable=format_var, values=['mp3', 'ogg'], state="readonly")
format_menu.pack(pady=5)

label = ttk.Label(root, text="Enter Text:")
label.pack(pady=10)
text_entry = tk.Text(root, height=10, width=40, wrap=tk.WORD)
text_entry.pack(pady=10)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

convert_button = ttk.Button(button_frame, text="Convert to Speech", command=convert_text)
convert_button.grid(row=0, column=0, padx=5, pady=5)

clear_button = ttk.Button(button_frame, text="Clear Text", command=clear_text)
clear_button.grid(row=0, column=1, padx=5, pady=5)

stop_button = ttk.Button(button_frame, text="Stop Audio", command=stop_audio)
stop_button.grid(row=1, column=0, padx=5, pady=5)

save_button = ttk.Button(button_frame, text="Save Text", command=save_text)
save_button.grid(row=1, column=1, padx=5, pady=5)

load_button = ttk.Button(button_frame, text="Load Text", command=load_text)
load_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()

pygame.mixer.quit()
