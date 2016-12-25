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
'''
Taken from https://github.com/jameslyons/python_speech_features, and added here. Extracts a 12 dimensional 
feature vector every .025 seconds (with a .015 window)
'''
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
'''
Taken from https://github.com/jameslyons/python_speech_features, and added here. Extracts a 12 dimensional feature vector 
from the original MFCC vector that includes the velocity of the window (if done once) and the acceleration (if done twice). 
'''
def delta(feat, N): #definition for delta function used in the MFCC feature extraction 
	NUMFRAMES = len(feat)
	feat = np.concatenate(([feat[0] for i in range(N)], feat, [feat[-1] for i in range(N)]))
	denom = sum([2*i*i for i in range(1,N+1)])
	dfeat = []
	for j in range(NUMFRAMES):
		dfeat.append(np.sum([n*feat[N+j+n] for n in range(-1*N,N+1)], axis=0)/denom)
	return dfeat

####################################

(rate,sig) = wav.read("TESTER/INDIAN/INDIAN.wav") #saves the rate and signals of the .wav file of the Indian accent group
mfcc_feat = mfcc(sig,rate, numcep = 12) #extracts a 12 dimensional vector every .025 seconds (with a .015 window) from the .wav file
d1_feat = delta(mfcc_feat, 2) #gets a 12 dimensional vector of the velocity 
d2_feat = delta(d1_feat,2) #gets a 12 dimensional vector of the acceleration 

X = pd.concat([pd.DataFrame(mfcc_feat),pd.DataFrame(d1_feat),pd.DataFrame(d2_feat)],  axis=1) #36 dimensional dataframe of the MFCC, Delta1 (first derivative), and Delta1 (second derivative)
X = preprocessing.scale(X) #scales each parameter of X, to normalize everything to be from between 0 and 1

gmmIndian = mixture.GaussianMixture(n_components = 10, max_iter=1000, tol = .01, warm_start = True) #creates a gaussian mixture model (GMM) of X, using 10 components
gmmIndian.fit(X) #fit the created GMM to X


####################################

(TestRate,TestSig) = wav.read("TESTER/AMERICAN/AMERICAN.wav") #saves the rate and signals of the .wav file of the American accent group
TestMFCC_Feat = mfcc(TestSig,TestRate,  numcep = 12) #extracts a 12 dimensional vector every .025 seconds (with a .015 window) from the .wav file
TestD1_FEAT = delta(TestMFCC_Feat, 2)#gets a 12 dimensional vector of the velocity 
TestD2_FEAT = delta(TestD1_FEAT,2) #gets a 12 dimensional vector of the acceleration 

A = pd.concat([pd.DataFrame(TestMFCC_Feat),pd.DataFrame(TestD1_FEAT),pd.DataFrame(TestD2_FEAT)],  axis=1) #36 dimensional dataframe of the MFCC, Delta1 (first derivative), and Delta1 (second derivative)
A = preprocessing.scale(A)#scales each parameter of A, to normalize everything to be from between 0 and 1

gmmAmerican = mixture.GaussianMixture(n_components = 10, max_iter=1000, tol = .01, warm_start = True) #creates a gaussian mixture model (GMM) of X, using 10 components
gmmAmerican.fit(A)#fit the created GMM to X

####################################

(newrate,newsig) = wav.read("Vincent.wav") #saves the rate and signals of the .wav file of the input 
Newmfcc_feat = mfcc(newsig,newrate, numcep = 12)#extracts a 12 dimensional vector every .025 seconds (with a .015 window) from the .wav file
Newd1_feat = delta(Newmfcc_feat, 2)#gets a 12 dimensional vector of the velocity 
Newd2_feat = delta(Newd1_feat,2)#gets a 12 dimensional vector of the acceleration

Z = pd.concat([pd.DataFrame(Newmfcc_feat),pd.DataFrame(Newd1_feat), pd.DataFrame(Newd2_feat)],  axis=1) #36 dimensional dataframe of the MFCC, Delta1 (first derivative), and Delta1 (second derivative)
Z = preprocessing.scale(Z)#scales each parameter of Z, to normalize everything to be from between 0 and 1

INDIAN = (gmmIndian.score_samples(Z)) #find the probability of Z in regards to the model of the indian accent
AMERICAN = (gmmAmerican.score_samples(Z)) #find the probability of Z in regards to the model of the american accent


####################################

STATES = pd.DataFrame({0 : xrange(0, len(INDIAN))}) #create a dataframe (numbers used are arbitrary)
for x in xrange(0,len(INDIAN)): #for loop that decides if the probability of a specific window of time in the input file is more indian or american, and assigns a 'state' to each. 0 is Indian, 1 is American
	if (INDIAN[x] > AMERICAN[x]):
		STATES[x:x+1] = 0;
	if (INDIAN[x] < AMERICAN[x]):
		STATES[x:x+1] = 1;

STATES = STATES.squeeze()
UnFormatedCounts = STATES.value_counts() 
print "UNFORMATTED COUNT:"
print UnFormatedCounts #displays total amount of 0's (Indian Accent) and 1's (American Accent)



'''
Below is an experimental algorithm to 'clean up' the state probability (assignment of 0's and 1's). 
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

if (UnFormatedCounts[0] > UnFormatedCounts[1]):
	Accent = 0
else:
	Accent = 1
	
STATES = pd.Series(STATES)
step = 4
for t in xrange(0,len(STATES),step):
	summer = STATES[t:(t+step)].sum()
	if (summer >= (step)/2):
		for p in xrange(t, t+step):
			STATES[p:p+1] = Accent

FormatedCounts = STATES.value_counts()
print"FORMATTED COUNT:"
print FormatedCounts

