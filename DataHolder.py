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

AUSTRALIAN = ["http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=131",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=136",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=140",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=148",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=485",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=525",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=529",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=533",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=776",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=961",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1072",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1085",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1352",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1377",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1547"]

TESTAUSTRALIAN = ["http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1733",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2104",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2172"]

TESTAMERICAN = ["http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=114",
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

TESTINDIAN = ["http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=199", 
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=198",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2286",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2350",
"http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=265"]
