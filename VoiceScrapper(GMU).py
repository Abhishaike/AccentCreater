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


INDIAN = ["http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=207",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=587",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=593",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=910",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1017",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1437",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1697",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1966",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2206",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2209",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2236",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2242",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2303",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2353",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2354"]



AMERICAN = ["http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=61",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=110",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=132",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=73",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=74",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=76",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=81",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=83",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=84",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=92",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=95",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=105",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=106",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=109",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=112"]

'''

"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=114",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=120",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=122",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=124",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=125",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=127",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=128",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=129",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=130",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=133",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=134",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=137",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=138",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=142",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=145"]

'''

IndianCombined = AudioSegment.empty()
for x in INDIAN:
	page = urllib.urlopen(x, 'lxml')
	html = page.read()
	soup = BeautifulSoup(html)
	x = soup.audio.source
	y = x.get('src')
	urllib.urlretrieve (y, "TESTER/INDIAN/INDIAN.mp3")
	AudioSegment.from_mp3("TESTER/INDIAN/INDIAN.mp3").export("TESTER/INDIAN/INDIAN.wav", format="wav")
	sound = AudioSegment.from_file("TESTER/INDIAN/INDIAN.wav")
	IndianCombined += sound

IndianCombined.export("TESTER/INDIAN/INDIAN.wav", format='wav')


AmericanCombined = AudioSegment.empty()
for x in AMERICAN:
	page = urllib.urlopen(x, 'lxml')
	html = page.read()
	soup = BeautifulSoup(html)
	x = soup.audio.source
	y = x.get('src')
	urllib.urlretrieve (y, "TESTER/AMERICAN/AMERICAN.mp3")
	AudioSegment.from_mp3("TESTER/AMERICAN/AMERICAN.mp3").export("TESTER/AMERICAN/AMERICAN.wav", format="wav")
	sound = AudioSegment.from_file("TESTER/AMERICAN/AMERICAN.wav")
	AmericanCombined += sound

AmericanCombined.export("TESTER/AMERICAN/AMERICAN.wav", format='wav')
