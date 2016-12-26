# AccentCreater

MFCC_Delta_Definition.py: Defines the functions for finding the MFCC (Mel-Frequency-Cepstral-Coefficient) and the Delta's of the MFCC's

VoiceScrapper.py: Holds the scripts neccesary to automatically extract the mp3 files of a given link, convert it to .wav format, and save it. A numpy array is used to hold the links initially (links are stored in DataHolder.py). These links are derived using the Chrome web-app Scrapper. This currently holds the 

DataHolder.py: Holds the collection of accent-categorized GMU links. These are seperated into [AccentName] and TEST[AccentName]. The later is used to test the predictive power of the model used. 

ModelCreation.py: Functions to extract the MFCC's, D's, and DD's of all the currently supported accents, concetenate them into a single dataframe, and fit a Gaussian Mixture Model to it. A seperate Gaussian Mixture Model is fitted for each accent. 

AccentScore.py: 'Scores' the input audio file against two models: the accent the user has, and the accent the user wants to have. Outputs a Pandas Series with window-by-window breakdown of what the audio file has been classified as. Employs a currently experimental algorithim to 'clean up' this Series to make it possible to better identify collections of accent dichotomies. 
