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

for z in TESTAUSTRALIAN:
	page = urllib.urlopen(z, 'lxml')
	html = page.read()
	soup = BeautifulSoup(html)
	p = soup.audio.source
	y = p.get('src')
	urllib.urlretrieve (y, "TESTER/TEST/TEST.mp3")
	AudioSegment.from_mp3("TESTER/TEST/TEST.mp3").export("TESTER/TEST/TEST.wav", format="wav")
	sound = AudioSegment.from_file("TESTER/TEST/TEST.wav")
	sound.export("TESTER/TEST/TEST.wav", format='wav')
	(newrate,newsig) = wav.read("TESTER/TEST/TEST.wav") #MFCC feature creation 
	Newmfcc_feat = mfcc(newsig,newrate, numcep = 12)
	Newd1_feat = delta(Newmfcc_feat, 2)
	Newd2_feat = delta(Newd1_feat,2)
	NEW_VOICE = pd.concat([pd.DataFrame(Newmfcc_feat),pd.DataFrame(Newd1_feat), pd.DataFrame(Newd2_feat)],  axis=1)
	NEW_VOICE = preprocessing.scale(NEW_VOICE)
	ACCENT_ONE_SCORE = (ACCENT_INDIAN.score_samples(NEW_VOICE))
	ACCENT_TWO_SCORE = (ACCENT_AUSTRALIAN.score_samples(NEW_VOICE))
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


