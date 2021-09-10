import os
import pyttsx3
from random import choice

engine = None


def init_tts():
    """
    Initializes the pytts engine
    :return:
    """
    global engine
    engine = pyttsx3.init()

def stop_tts():
    """
    Stops the pytts engine
    :return:
    """
    global engine
    engine.stop()

def read(text):
    """
    Converts text to speech in an mp3 file 
    using google or pyttsx3.
    Plays the mp3 file.
    :param text: The rext to read
    :return:
    """
    global engine
    engine.say(text)
    engine.runAndWait()


def playBang():
    os.system("afplay ./SoundEffects/Bang{}.m4a".format(choice([1, 2, 3, 4, 5])))

def playDunk():
    os.system("afplay ./SoundEffects/Dunk{}.m4a".format(choice([1,2,3,4,5])))

def playFreethrow():
    os.system("afplay ./SoundEffects/Freethrow{}.m4a".format(choice([1, 2, 3])))
