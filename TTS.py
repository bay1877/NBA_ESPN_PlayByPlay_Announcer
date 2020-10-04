# to speech conversion
from gtts import gTTS
# This module is imported so that we can
# play the converted audio
import os, random


def read(text):
    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=text, lang=language, slow=False)
    # Saving the converted audio in a mp3 file named
    # welcome
    myobj.save("play.mp3")
    # Playing the converted file
    os.system("afplay play.mp3")

def playBang():
    choice = random.choice([1, 2, 3, 4, 5])
    os.system("afplay ./SoundEffects/Bang{}.m4a".format(choice))

def playDunk():
    choice = random.choice([1,2,3,4,5])
    os.system("afplay ./SoundEffects/Dunk{}.m4a".format(choice))

def playFreethrow():
    choice = random.choice([1, 2, 3])
    os.system("afplay ./SoundEffects/Freethrow{}.m4a".format(choice))






