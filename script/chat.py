import sys
import importlib
import subprocess
import time
import os

def install(req_mod):
    python = sys.executable
    subprocess.check_output([python, '-m', 'pip', 'install', req_mod], stderr=subprocess.DEVNULL)

import_array = ['tkinter', 'openai', 'time', 'pygame', 'gtts']
for req in import_array:
    try:
        importlib.import_module(req)
    except ModuleNotFoundError:
        print("module '{}' is not installed, installing...".format(req))
        install(req)

import tkinter as tk
from tkinter import ttk
import gtts
import pygame
import openai
from typing import List
from gtts import gTTS


global akey
global mtvar
global tempvar
mtvar=384
akey="null"
tempvar=.7
model_id = "gpt-3.5-turbo"

def playback_translation():
    myobj = gTTS(text=ai_response, lang=language)
    myobj.save("welcome.mp3")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("welcome.mp3")
    pygame.mixer.music.play()

    input_frame.mainloop()

    pygame.mixer.quit()
    pygame.quit()
    os.remove("welcome.mp3")

def stop_playback():
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.quit()

def update_mt_status():
    global mtvar
    status_label_mtv.config(text=mtvar)

def update_t_status():
    global tempvar
    status_label_tvv.config(text=tempvar)

# Create conversation list with initial system prompt
def show_api_key_prompt():
    api_key_prompt_window = tk.Toplevel(window)
    api_key_prompt_window.title("API Key Prompt")
    api_key_label = tk.Label(api_key_prompt_window, text="Enter your API key:")
    api_key_label.pack(anchor="nw")
    api_key_entry = tk.Entry(api_key_prompt_window,  width=50)
    api_key_entry.pack(side=tk.LEFT, pady=5, padx=5)

    def submit_api_key():
        api_key = api_key_entry.get()
        get_api_key(api_key)
        update_key()
        update_api_status("API Status: Ready")
        api_key_prompt_window.destroy()

    submit_button = tk.Button(api_key_prompt_window, text="Submit", command=submit_api_key)
    submit_button.pack(side=tk.LEFT, pady=5, padx=5)

conversation_prompt = "You are a brilliant assistant who is an expert in cybersecurity."
conversation = [{"role": "system", "content": conversation_prompt}]

def on_button_click():
    global ai_response
    user_input = input_text.get("1.0", tk.END).strip()  # Retrieve the user input from the Text widget
    if user_input != "":
        conversation.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=conversation,
            max_tokens=mtvar,
            temperature=tempvar,
            top_p=1.0,
            n=1,
            stop=None,
        )
        
        ai_response = response.choices[0].message.content
        display_text.insert(tk.END, "User: " + user_input + "\n")
        display_text.insert(tk.END, "AI: " + ai_response + "\n") 
        display_text.insert(tk.END, "====================" +"\n")
        conversation.append({"role": "assistant", "content": ai_response})
        time.sleep(1)
        input_text.delete("1.0", tk.END)  # Clear the user input Text widget
        scroll_to_bottom()

def a_select(event):
    global language
    accent_opt = accent_dd.get()
    if accent_opt == "English":
        language = "en"
    elif accent_opt == "Spanish":
        language = "es"
    elif accent_opt == "French":
        language = "fr"
    elif accent_opt == "German":
        language = "de"
    elif accent_opt == "Korean":
        language = "ko"
    elif accent_opt == "Japanese":
        language = "ja"
    elif accent_opt == "Filipino":
        language = "tl"
    elif accent_opt == "Russian":
        language = "ru"
    elif accent_opt == "Chinese":
        language = "zh-TW"    

# Create the main window
window = tk.Tk()
window.title("OpenAI Chat Client")

# Create Notebook with Tabs
notebook = ttk.Notebook(window)

# Tab 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text=" Chat ")

# User Input
input_frame = ttk.Frame(tab1)
input_frame.pack(side=tk.TOP, anchor="nw", pady=5)
input_text = tk.Text(input_frame, height=5, width=65)
input_text.pack(side=tk.LEFT, padx=5, pady=0)

language="en"
accent_dd_fr = ttk.Frame(tab1)
accent_dd_lb = ttk.Label(accent_dd_fr, text="Playback Accent")
accent_dd_lb.pack(side=tk.LEFT)
accent_var=tk.StringVar(accent_dd_fr)
accent_dd = ttk.Combobox(accent_dd_fr, textvariable=language)
accent_dd['values'] = ("English","Spanish","French","German","Korean","Japanese","Filipino","Russian","Chinese")
accent_dd.bind("<<ComboboxSelected>>", a_select)
accent_dd.pack(side=tk.LEFT, padx=20, pady=5)

# Send Button
button = ttk.Button(input_frame, text="Send", command=on_button_click)
button.pack(side=tk.TOP, padx=5)
trans_stop = ttk.Button(input_frame, text="Stop", command=stop_playback)
trans_stop.pack(side=tk.BOTTOM, padx=5)
trans = ttk.Button(input_frame, text="Play", command=playback_translation)
trans.pack(side=tk.BOTTOM, padx=5)

accent_dd_fr.pack(side=tk.BOTTOM)

# Conversation Window
display_frame = ttk.Frame(tab1)
def scroll_to_bottom():
    display_text.yview_moveto(1.0)

scrollbar = tk.Scrollbar(display_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
display_text = tk.Text(display_frame, height=45, width=80, yscrollcommand=scrollbar.set)
scrollbar.config(command=display_text.yview)
display_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
display_frame.pack(side=tk.LEFT, anchor="ne", fill=tk.BOTH, expand=True,pady=5, padx=5)

#Tab 2
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Settings")

#Temperature Slider
def ts_slider_move(ts_value):
    global tempvar
    print(ts_value)
    tempvar=float(ts_value)
    update_t_status()
ts_frame = ttk.Frame(tab2)
ts_label = ttk.Label(ts_frame, text="Temperature")
ts_label.pack(side=tk.LEFT)
tempslid = tk.Scale(ts_frame, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=ts_slider_move)
tempslid.set(.7)
tempslid.pack(side=tk.LEFT, padx=20, pady=5)

#Max Tokens Slider
def mt_slider_move(mt_value):
    global mtvar
    global mtsvar
    print(mt_value)
    mtvar=int(mt_value)
    update_mt_status()

mt_frame = ttk.Frame(tab2)
mt_label = ttk.Label(mt_frame, text="Max Tokens ")
mt_label.pack(side=tk.LEFT)
tokslid = tk.Scale(mt_frame, from_=64, to=2048, resolution=64, orient=tk.HORIZONTAL, command=mt_slider_move)
tokslid.set(384)
tokslid.pack(side=tk.LEFT, padx=20, pady=5)

#Current API key
def update_key():
    global ak_text
    first = akey[0:6]
    b = len(akey)
    a = b - 6
    c = a - 6
    fill = '*' * c
    last = akey[a:b]
    obkey = first+fill+last
    ak_text.delete("1.0", tk.END)
    ak_text.insert(tk.END, obkey)

ak_frame = ttk.Frame(tab2)
ak_label = ttk.Label(ak_frame, text="API Key")
ak_label.pack(side=tk.LEFT)
ak_text = tk.Text(ak_frame, height=1, width=54)
ak_text.insert(tk.END, akey)
ak_text.pack(side=tk.LEFT, padx=20, pady=10)

#Statusbar Sections
status_frame = tk.Frame(window, bd=1, relief=tk.SUNKEN)
status_frame.pack(side=tk.BOTTOM, fill=tk.X)

status_label_api = tk.Label(status_frame, text="API: No Key", bd=0, relief=tk.SUNKEN, anchor=tk.W)
status_label_mtl = tk.Label(status_frame, text="Max Tokens: ", bd=0, relief=tk.SUNKEN, anchor=tk.W)
status_label_mtv = tk.Label(status_frame, text=mtvar, bd=0, relief=tk.SUNKEN, anchor=tk.W)
status_label_tvl = tk.Label(status_frame, text="Temperature: ", bd=0, relief=tk.SUNKEN, anchor=tk.W)
status_label_tvv = tk.Label(status_frame, text=tempvar, bd=0, relief=tk.SUNKEN, anchor=tk.W)

status_label_api.pack(side=tk.LEFT, padx=4, pady=2, fill=tk.X)
status_label_mtl.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.X)
status_label_mtv.pack(side=tk.LEFT, padx=4, pady=2, fill=tk.X)
status_label_tvl.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.X)
status_label_tvv.pack(side=tk.LEFT, padx=4, pady=2, fill=tk.X)

# Model select
def model_select(event):
    global model_id
    selected_option = model_dd.get()
    if selected_option == "ChatGPT 3.5 Turbo":
        model_id = "gpt-3.5-turbo"    
    elif selected_option == "ChatGPT 4.0":
        model_id = "gpt-4-0613"

model_dd_frame = ttk.Frame(tab2)
model_dd_label = ttk.Label(model_dd_frame, text="Select Model")
model_dd_label.pack(side=tk.LEFT)
variable = tk.StringVar(model_dd_frame)
model_dd = ttk.Combobox(model_dd_frame, textvariable=model_id)
model_dd['values'] = ("ChatGPT 3.5 Turbo", "ChatGPT 4.0")
model_dd.bind("<<ComboboxSelected>>", model_select)
model_dd.pack(side=tk.LEFT, padx=20, pady=5)
open_prompt_button = tk.Button(ak_frame, text="Change API Key", command=show_api_key_prompt)
open_prompt_button.pack(side=tk.LEFT, padx=5)

#Pre-Defined conversation Prompts
def cp_select(event):
    global conversation_prompt
    global conversation
    selected_option = prompt_dd.get()
    if selected_option == "Cybersecurity":
        conversation_prompt = "You are a brilliant assistant who is an expert in cybersecurity."
        conversation = [{"role": "system", "content": conversation_prompt}]
    elif selected_option == "Author":
        conversation_prompt = "You are creative author, with a flare for world creation"
        conversation = [{"role": "system", "content": conversation_prompt}]
    elif selected_option == "Communicator":
        conversation_prompt = "Translate into a brief Email"
        conversation = [{"role": "system", "content": conversation_prompt}]

#User input converstion prompt
def cp_submit():
    global conversation
    cp_input = cp_ui_text.get("1.0", tk.END).strip()
    conversation = [{"role": "system", "content": cp_input}]

cp_dd_frame = ttk.Frame(tab2)
cp_dd_label = ttk.Label(cp_dd_frame, text="Select  Mode")
cp_dd_label.pack(side=tk.LEFT)
variable = tk.StringVar(cp_dd_frame)
prompt_dd = ttk.Combobox(cp_dd_frame, textvariable=conversation_prompt)
prompt_dd['values'] = ("Cybersecurity", "Author", "Communicator")
prompt_dd.bind("<<ComboboxSelected>>", cp_select)
prompt_dd.pack(side=tk.LEFT, padx=20, pady=5)

cp_ui_frame = ttk.Frame(tab2)
cp_ui_label = ttk.Label(cp_ui_frame, text="Custom Mode")
cp_ui_label.pack(side=tk.LEFT, pady=10)
cp_ui_text = tk.Text(cp_ui_frame, height=3, width=50)
cp_ui_text.pack(side=tk.LEFT, pady=0, padx=20)
cp_bt_frame = ttk.Frame(tab2)
cp_ui_button = tk.Button(cp_ui_frame, text="Submit", command=cp_submit)
cp_ui_button.pack(side=tk.BOTTOM)

#Statusbar functions
def get_api_key(api_key):
    global akey
    print("API Key stored")
    openai.api_key=api_key
    akey = openai.api_key
        
def update_api_status(vartext):
    status_label_api.config(text=vartext)

def check_env_var(key_var):
    api_key = os.getenv(key_var)
    if api_key is not None:
        get_api_key(api_key)
        update_key()
        update_api_status("API Status: Ready")
    else:
        get_api_key("null")
        update_api_status("API Status: No Key")
        
check_env_var("OPENAI_API_KEY")

ak_frame.pack(anchor="nw")
cp_ui_frame.pack(anchor="nw")
cp_dd_frame.pack(anchor="nw")
model_dd_frame.pack(anchor="nw")
ts_frame.pack(anchor="nw")
mt_frame.pack(anchor="nw")
notebook.pack()

# Start the GUI event loop
window.mainloop()
