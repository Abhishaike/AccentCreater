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
def mfcc(signal,samplerate=16000,winlen=0.025,winstep=0.01,numcep=13,
         nfilt=26,nfft=512,lowfreq=0,highfreq=None,preemph=0.97,ceplifter=22,appendEnergy=False,
         winfunc=lambda x:np.ones((x,))):
    feat,energy = fbank(signal,samplerate,winlen,winstep,nfilt,nfft,lowfreq,highfreq,preemph,winfunc)
    feat = np.log(feat)
    feat = dct(feat, type=2, axis=1, norm='ortho')[:,:numcep]
    feat = lifter(feat,ceplifter)
    if appendEnergy: feat[:,0] = np.log(energy) # replace first cepstral coefficient with log of frame energy
    return feat

####################################

def delta(feat, N): #definition for delta function used in the MFCC feature extraction 
	NUMFRAMES = len(feat)
	feat = np.concatenate(([feat[0] for i in range(N)], feat, [feat[-1] for i in range(N)]))
	denom = sum([2*i*i for i in range(1,N+1)])
	dfeat = []
	for j in range(NUMFRAMES):
		dfeat.append(np.sum([n*feat[N+j+n] for n in range(-1*N,N+1)], axis=0)/denom)
	return dfeat
