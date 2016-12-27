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

script, filename = argv

FILE_PATH = open(filename)

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


'''
Above is an experimental algorithm to 'clean up' the state probability (assignment of 0's and 1's). 
This algorithim operates under the assumption that, with the 'curse of dimensionality', the log probability of any given 
'score' will be extremely low. Only with a holisitic approach to ALL the probabilities can you know which classification the 
entire input file is. And that's how many academic papers have approached this issue in the past, by only paying attention to
the classification of the entire input audio file, rather than looking at the accuracy of single windows of time (.025 seconds).
This algorithm allows one to correct *possible* mistakes in the intial classification by forcing a bias on the dataset: that 
the input file is either one accent or the other. This bias can be figured out through the usual method: looking at all the 
probabilities. Once you know this (the algorithm automatically does it), it will begin using a 'step' size to 'correct' mistakes
in the initial classification. The step size is a array-window that automatically changes everything within that window to the
majority state value. 
For example, let's say the classification of an audio file was the following: 

1 1 1 1 0 1 1 0 1 1 0 1 0 0 0 0

1's = 9
0's = 7

Obviously, the audio file should be classified as having an accent of 1, as there are clearly more 1's overall. However, now it 
looks like the audio file suddenly goes through a change in accent from 1 to 0 in three places, when, in reality, a change of
accent (phonemes) cannot occur on a .025 window. It was likely the result of extremely high dimensionality which caused this
'suddenly' incorrect classification, and it misrepresents the dataset. 

However, if we use a step-size of 5, which would mean 5 array spots, which would then mean a likely phoneme change every 
.125 seconds,that sounds a little more reasonable. Let's first split the array with a step size of 5:

ORIGINAL:
1 1 1 1 0 
1 1 0 1 1 
0 1 0 0 0 
0

There is a majority of 1's on the first row, a majority of 1's on the second, a majority of 0's on the third, and
(obviously), a majority of 0's on the fourth. Thus, the formated verison is then : 

CONVERTED: 
1 1 1 1 1 
1 1 1 1 1 
0 0 0 0 0 
0

1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0

1's: 10
0's: 6

That seems a little more reasonable. A string of 1's, and then 0's at the end. This is an improvement on the traditional holistic
method, as it allows us to look closer at the more probable areas where the accent changes (more linguistically possible). 

'''


