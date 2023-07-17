import os
import sys
import importlib
import subprocess
import playsound

def install(req_mod):
    python = sys.executable
    subprocess.check_output([python, '-m', 'pip', 'install', req_mod], stderr=subprocess.DEVNULL)

import_array = ['gtts','playsound']
for req in import_array:
    try:
        importlib.import_module(req)
    except ModuleNotFoundError:
        print("module '{}' is not installed, installing...".format(req))
        install(req)

from gtts import gTTS
from playsound import playsound

mytext = "This is a test"
language = 'tl'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("welcome.mp3")
playsound('welcome.mp3')
