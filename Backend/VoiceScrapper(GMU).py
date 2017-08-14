from sklearn.mixture import GMM
from sklearn import mixture
from python_speech_features import mfcc
from python_speech_features import logfbank
from python_speech_features import ssc
from python_speech_features import fbank
from python_speech_features import lifter

from scipy.fftpack import dct
import pandas as pd
import numpy as np
import scipy.io.wavfile as wav
import wave
from pydub import AudioSegment
from sklearn import preprocessing
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib
import urllib2
import requests 

import DataHolder


IndianCombined = AudioSegment.empty()
for x in DataHolder.INDIAN:
	page = urllib.urlopen(x, 'lxml')
	html = page.read()
	soup = BeautifulSoup(html, "html.parser")
	x = soup.audio.source
	y = x.get('src')
	urllib.urlretrieve(y, "TESTER/INDIAN/INDIAN.mp3")
	AudioSegment.from_mp3("TESTER/INDIAN/INDIAN.mp3").export("TESTER/INDIAN/INDIAN.wav", format="wav")
	sound = AudioSegment.from_file("TESTER/INDIAN/INDIAN.wav")
	IndianCombined += sound

IndianCombined.export("TESTER/INDIAN/INDIAN.wav", format='wav')


AmericanCombined = AudioSegment.empty()
for x in DataHolder.AMERICAN:
	page = urllib.urlopen(x, 'lxml')
	html = page.read()
	soup = BeautifulSoup(html, "html.parser")
	x = soup.audio.source
	y = x.get('src')
	urllib.urlretrieve (y, "TESTER/AMERICAN/AMERICAN.mp3")
	AudioSegment.from_mp3("TESTER/AMERICAN/AMERICAN.mp3").export("TESTER/AMERICAN/AMERICAN.wav", format="wav")
	sound = AudioSegment.from_file("TESTER/AMERICAN/AMERICAN.wav")
	AmericanCombined += sound

AmericanCombined.export("TESTER/AMERICAN/AMERICAN.wav", format='wav')


AustralianCombined = AudioSegment.empty()
for x in DataHolder.AUSTRALIAN:
	page = urllib.urlopen(x, 'lxml')
	html = page.read()
	soup = BeautifulSoup(html, "html.parser")
	x = soup.audio.source
	y = x.get('src')
	urllib.urlretrieve (y, "TESTER/AUSTRALIAN/AUSTRALIAN.mp3")
	AudioSegment.from_mp3("TESTER/AUSTRALIAN/AUSTRALIAN.mp3").export("TESTER/AUSTRALIAN/AUSTRALIAN.wav", format="wav")
	sound = AudioSegment.from_file("TESTER/AUSTRALIAN/AUSTRALIAN.wav")
	AustralianCombined += sound

AustralianCombined.export("TESTER/AUSTRALIAN/AUSTRALIAN.wav", format='wav')
