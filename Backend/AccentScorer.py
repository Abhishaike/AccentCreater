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
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib
import urllib2
import requests 
from sys import argv


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

####################################

def AccentScorer(FILE_PATH, ACCENT_MODEL_1, ACCENT_MODEL_2):
	AudioSegment.from_mp3(FILE_PATH).export("TESTER/TEST/TEST.wav", format="wav")
	sound = AudioSegment.from_file("TESTER/TEST/TEST.wav")
	sound.export("TESTER/TEST/TEST.wav", format='wav')
	(RATE_INPUT,SIG_INPUT) = wav.read("TESTER/TEST/TEST.wav") #MFCC feature creation 
	ACCENT_MFCC_INPUT = mfcc(SIG_INPUT,RATE_INPUT, numcep = 12)
	ACCENT_DELTA_INPUT = delta(ACCENT_MFCC_INPUT, 2)
	ACCENT_DELTA2_INPUT = delta(ACCENT_DELTA_INPUT,2)
	NEW_VOICE = pd.concat([pd.DataFrame(ACCENT_MFCC_INPUT),pd.DataFrame(ACCENT_DELTA_INPUT), pd.DataFrame(ACCENT_DELTA2_INPUT)],  axis=1)
	NEW_VOICE = preprocessing.scale(NEW_VOICE)
	ACCENT_ONE_SCORE = (ACCENT_MODEL_1.score_samples(NEW_VOICE))
	ACCENT_TWO_SCORE = (ACCENT_MODEL_2.score_samples(NEW_VOICE))
	STATES = pd.DataFrame({0 : xrange(0, len(ACCENT_ONE_SCORE))})
	for x in xrange(0,len(ACCENT_ONE_SCORE)):
		if (ACCENT_ONE_SCORE[x] > ACCENT_TWO_SCORE[x]):
			STATES[x:x+1] = 0;
		if (ACCENT_ONE_SCORE[x] < ACCENT_TWO_SCORE[x]):
			STATES[x:x+1] = 1;
	STATES = STATES.squeeze()
	UnFormatedCounts = STATES.value_counts()
	print "UNFORMATTED COUNT:"
	print UnFormatedCounts
	if (UnFormatedCounts[0] > UnFormatedCounts[1]):
		Accent = 0
	else:
		Accent = 1
	STATES = pd.Series(STATES)
	step = 8
	for t in xrange(0,len(STATES),step):
		summer = STATES[t:(t+step)].sum()
		if (summer >= (step)/2):
			for p in xrange(t, t+step):
				STATES[p:p+1] = Accent
	FormatedCounts = STATES.value_counts()
	print"FORMATTED COUNT:"
	print FormatedCounts
	return FormatedCounts
