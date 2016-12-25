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

####################################

(rate,sig) = wav.read("TESTER/INDIAN/INDIAN.wav")
mfcc_feat = mfcc(sig,rate, numcep = 12)
d1_feat = delta(mfcc_feat, 2)
d2_feat = delta(d1_feat,2)

X = pd.concat([pd.DataFrame(mfcc_feat),pd.DataFrame(d1_feat),pd.DataFrame(d2_feat)],  axis=1) #39 dimensional dataframe of the MFCC, Delta1 (first derivative), and Delta1 (second derivative)
X = preprocessing.scale(X)

gmmIndian = mixture.GaussianMixture(n_components = 10, max_iter=1000, tol = .01, warm_start = True)
gmmIndian.fit(X)


####################################

(TestRate,TestSig) = wav.read("TESTER/AMERICAN/AMERICAN.wav") #MFCC feature creation 
TestMFCC_Feat = mfcc(TestSig,TestRate,  numcep = 12)
TestD1_FEAT = delta(TestMFCC_Feat, 2)
TestD2_FEAT = delta(TestD1_FEAT,2)

A = pd.concat([pd.DataFrame(TestMFCC_Feat),pd.DataFrame(TestD1_FEAT),pd.DataFrame(TestD2_FEAT)],  axis=1)
A = preprocessing.scale(A)

gmmAmerican = mixture.GaussianMixture(n_components = 10, max_iter=1000, tol = .01, warm_start = True)
gmmAmerican.fit(A)

####################################

page = urllib.urlopen("http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=426", 'lxml')
html = page.read()
soup = BeautifulSoup(html)
x = soup.audio.source
y = x.get('src')
urllib.urlretrieve (y, "TESTER/INDIAN/INDIANTEST.mp3")
AudioSegment.from_mp3("TESTER/INDIAN/INDIANTEST.mp3").export("TESTER/INDIAN/INDIANTEST.wav", format="wav")
sound = AudioSegment.from_file("TESTER/INDIAN/INDIANTEST.wav")
sound.export("TESTER/INDIAN/INDIANTEST.wav", format='wav')


(newrate,newsig) = wav.read("Vincent.wav") #MFCC feature creation 
Newmfcc_feat = mfcc(newsig,newrate, numcep = 12)
Newd1_feat = delta(Newmfcc_feat, 2)
Newd2_feat = delta(Newd1_feat,2)

Z = pd.concat([pd.DataFrame(Newmfcc_feat),pd.DataFrame(Newd1_feat), pd.DataFrame(Newd2_feat)],  axis=1)
Z = preprocessing.scale(Z)

INDIAN = (gmmIndian.score_samples(Z))
AMERICAN = (gmmAmerican.score_samples(Z))


####################################

STATES = pd.DataFrame({0 : xrange(0, len(INDIAN))})
for x in xrange(0,len(INDIAN)):
	if (INDIAN[x] > AMERICAN[x]):
		STATES[x:x+1] = 0;
	if (INDIAN[x] < AMERICAN[x]):
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
step = 4
for t in xrange(0,len(STATES),step):
	summer = STATES[t:(t+step)].sum()
	if (summer >= (step)/2):
		for p in xrange(t, t+step):
			STATES[p:p+1] = Accent

FormatedCounts = STATES.value_counts()
print"FORMATTED COUNT:"
print FormatedCounts

