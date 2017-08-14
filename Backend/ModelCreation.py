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

####################################

(rate,sig) = wav.read("TESTER/INDIAN/INDIAN.wav")
MFCC_ACCENT_INDIAN = mfcc(sig,rate, numcep = 12)
DELTA_ACCENT_INDIAN = delta(MFCC_ACCENT_INDIAN, 2)
DELTA2_ACCENT_INDIAN = delta(DELTA_ACCENT_INDIAN,2)

ACCENT_INDIAN_FEATURES = pd.concat([pd.DataFrame(MFCC_ACCENT_INDIAN),pd.DataFrame(DELTA_ACCENT_INDIAN),pd.DataFrame(DELTA2_ACCENT_INDIAN)],  axis=1) #39 dimensional dataframe of the MFCC, Delta1 (first derivative), and Delta1 (second derivative)
ACCENT_INDIAN_FEATURES = preprocessing.scale(ACCENT_INDIAN_FEATURES)

ACCENT_INDIAN = mixture.GaussianMixture(n_components = 35, max_iter=1000, tol = .01, warm_start = True, covariance_type = 'diag')
ACCENT_INDIAN.fit(ACCENT_INDIAN_FEATURES)


####################################

(TestRate,TestSig) = wav.read("TESTER/AMERICAN/AMERICAN.wav") #MFCC feature creation 
MFCC_ACCENT_AMERICAN = mfcc(TestSig,TestRate,  numcep = 12)
DELTA_ACCENT_AMERICAN = delta(MFCC_ACCENT_AMERICAN, 2)
DELTA2_ACCENT_AMERICAN = delta(DELTA_ACCENT_AMERICAN,2)

ACCENT_AMERICAN_FEATURES = pd.concat([pd.DataFrame(MFCC_ACCENT_AMERICAN),pd.DataFrame(DELTA_ACCENT_AMERICAN),pd.DataFrame(DELTA2_ACCENT_AMERICAN)],  axis=1)
ACCENT_AMERICAN_FEATURES = preprocessing.scale(ACCENT_AMERICAN_FEATURES)

ACCENT_AMERICAN = mixture.GaussianMixture(n_components = 35, max_iter=1000, tol = .01, warm_start = True, covariance_type = 'diag')
ACCENT_AMERICAN.fit(ACCENT_AMERICAN_FEATURES)

####################################

(TestRate,TestSig) = wav.read("TESTER/AUSTRALIAN/AUSTRALIAN.wav") #MFCC feature creation 
MFCC_ACCENT_AUSTRALIAN = mfcc(TestSig,TestRate,  numcep = 12)
DELTA_ACCENT_AUSTRALIAN = delta(MFCC_ACCENT_AUSTRALIAN, 2)
DELTA2_ACCENT_AUSTRALIAN = delta(DELTA_ACCENT_AUSTRALIAN,2)

ACCENT_AUSTRALIAN_FEATURES = pd.concat([pd.DataFrame(MFCC_ACCENT_AUSTRALIAN),pd.DataFrame(DELTA_ACCENT_AUSTRALIAN),pd.DataFrame(DELTA2_ACCENT_AUSTRALIAN)],  axis=1)
ACCENT_AUSTRALIAN_FEATURES = preprocessing.scale(ACCENT_AUSTRALIAN_FEATURES)

ACCENT_AUSTRALIAN = mixture.GaussianMixture(n_components = 35, max_iter=1000, tol = .01, warm_start = True, covariance_type = 'diag' )
ACCENT_AUSTRALIAN.fit(ACCENT_AUSTRALIAN_FEATURES)
