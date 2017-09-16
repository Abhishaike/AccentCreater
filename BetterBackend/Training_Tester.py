from watson_developer_cloud import SpeechToTextV1
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
import keras
import librosa
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from keras.models import Sequential
from keras.models import load_model
import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
from pydub import AudioSegment
import os.path
import os
from sklearn.model_selection import train_test_split
import h5py

def main(FILEPATH): #currently, WordEncoder is depreciated due to shitty the shitty sklearn LabelEncoder technique; unique words in testing data cause errors
    IBM_USERNAME = ""
    IBM_PASSWORD = ""
    stt = SpeechToTextV1(username=IBM_USERNAME, password=IBM_PASSWORD)
    if not os.path.exists('LSTM_MODEL_ARCHITECTURE_WEIGHTS.h5'): #if model doesnt exist, get the model created and trained
        AllWords_Training, AllAccents_Training, WordEncoder, AccentEncoder = CreateTrainingData()
        Train_and_Pickle_NN(AllWords_Training, AllAccents_Training)

    AllWords_Training, AllAccents_Training, WordEncoder, AccentEncoder = Load_Up() #loads all of these variables from the pickled files
    AllWords_Testing, SentenceCreated = CreateTestingData(FILEPATH, AllWords_Training, WordEncoder, AccentEncoder) #creates testing data from the previous
    AllPredictions_Word = Test(AllWords_Testing, SentenceCreated) #predicts accent labels for all testing data, and return a tuple of (word, array_of_predictions_per_accent)
    return AllPredictions_Word


def Train_and_Pickle_NN(AllWords_Training, AllAccents_Training) :
    #X_train, X_test, y_train, y_test = train_test_split(AllWords_Training_1, AllAccents_Training_1, test_size = 0.10, random_state = 42, stratify = AllAccents_Training_1)
    model = Sequential()
    model.add(LSTM(256, activation='sigmoid',recurrent_activation='tanh', stateful=False, return_sequences=True, input_shape=(AllWords_Training.shape[1], AllWords_Training.shape[2])))
    model.add(Dropout(.7))
    model.add(LSTM(256, activation='sigmoid',recurrent_activation='tanh', return_sequences=True))
    model.add(Dropout(.7))
    model.add(LSTM(256, activation='sigmoid',recurrent_activation='tanh', return_sequences=False))  # false because we want prediction per sequence, not per time-step
    model.add(Dropout(.7))
    model.add(Dense(5, activation='softmax'))
    rms = keras.optimizers.RMSprop(lr=0.001)
    model.compile(loss='categorical_crossentropy', optimizer=rms, metrics=['accuracy'])
    model.fit(AllWords_Training, AllAccents_Training, epochs = 30, batch_size=200, verbose=2, validation_data = (X_test, y_test))

    model.save('LSTM_MODEL_ARCHITECTURE_WEIGHTS.h5')


def Test(AllWords_Testing, SentenceCreated, AccentEncoder):
    model = keras.models.load_model('LSTM_MODEL_ARCHITECTURE_WEIGHTS.h5')
    AllPredictions_NoWord = []
    for Word, WordData in enumerate(AllWords_Testing):
        Predictions =  model.predict(np.reshape(WordData,(1, WordData.shape[0], WordData.shape[1])))
        AllPredictions_NoWord.append(list(zip(AccentEncoder.classes_, Predictions[0])))

    AllPredictions_Word = list(zip(SentenceCreated, AllPredictions_NoWord))
    return AllPredictions_Word


def CreateTrainingData():
    AllWords_Training = []
    AllAccents_Training = []
    for AccentInfo, AccentName in [(AMERICAN, "AMERICAN"),
                                   (INDIAN, "INDIAN"),
                                   (AUSTRALIAN, "AUSTRALIAN"),
                                   (MANDARIN, "MANDARIN"),
                                   (RUSSIAN, "RUSSIAN")]: #these tuples represent all the accents being tested/trained
        for PersonLink in AccentInfo:
            print (AccentName)
            page = urlopen(PersonLink, data= None)
            html = page.read()
            soup = BeautifulSoup(html, "html.parser")
            x = soup.audio.source
            y = x.get('src')
            urllib.request.urlretrieve (y, "test1.mp3")
            AudioSegment.from_mp3("test1.mp3").export("test1.wav", format="wav") #open link, save it to a dummy .mp3 file, convert to .wav, and get audiosegment of it

            audio_file = open('test1.wav', "rb")
            test_result = stt.recognize(audio_file,
                                   content_type="audio/wav",
                                   timestamps=True,
                                   profanity_filter = False) #send .wav file to IBM Watson API, which returns the timestampts of each word in it.

            sound_file = AudioSegment.from_wav('test1.wav')
            for Number, SingleTranscript in enumerate(test_result['results']): #for each single transcript in the IBM return dictionary
                for Words in SingleTranscript['alternatives'][0]['timestamps']: #for each word in a given transcript
                    NewWord = np.array(FeatureExtractor(Words, sound_file))
                    AllWords_Training.append(NewWord)
                    AllAccents_Training.append(AccentName)

    WordEncoder = LabelEncoder().fit([item[-1][-1] for item in AllWords_Training]) #turns all unique words into 'classes'
    for Word in range(len(AllWords_Training)):
        for Row in range(len(AllWords_Training[Word])):
            AllWords_Training[Word][Row][-1] = WordEncoder.transform([AllWords_Training[Word][Row][-1]])[0] #just....labelencoder is weird, don't question why you did this

    AccentEncoder = LabelEncoder().fit(AllAccents_Training) #turns all unique accents into 'classes'
    AllAccents_Training = AccentEncoder.transform(AllAccents_Training)

    AllWords_Training = keras.preprocessing.sequence.pad_sequences(AllWords_Training, dtype='object', padding = 'pre')
    AllWords_Training = np.delete(AllWords_Training, np.s_[-1], axis=2)

    AllAccents_Training = AllAccents_Training.copy()
    AllAccents_Training.reshape((-1, 1))
    AllAccents_Training = np_utils.to_categorical(AllAccents_Training)  # turns this into a one-hot vector.

    with open('AllWords_Training.pkl', 'wb') as f:
        pickle.dump(AllWords_Training, f)
    with open('AllAccents_Training.pkl', 'wb') as f:
        pickle.dump(AllAccents_Training, f)
    with open('WordEncoder.pkl', 'wb') as f:
        pickle.dump(WordEncoder, f)
    with open('AccentEncoder.pkl', 'wb') as f:
        pickle.dump(AccentEncoder, f)

    return AllWords_Training, AllAccents_Training, WordEncoder, AccentEncoder



def CreateTestingData(FILEPATH, AllWords_Training, WordEncoder, AccentEncoder):
    AllWords_Testing = []
    SentenceCreated = []
    AudioSegment.from_file(FILEPATH, "mp4").export("test1.wav",format="wav")  # open link, save it to a dummy .mp3 file, convert to .wav, and get audiosegment of it
    audio_file = open('test1.wav', "rb")
    test_result = stt.recognize(audio_file,
                                content_type="audio/wav",
                                timestamps=True,
                                profanity_filter=False)  # send .wav file to IBM Watson API, which returns the timestampts of each word in it.

    sound_file = AudioSegment.from_wav('test1.wav')
    for Number, SingleTranscript in enumerate(test_result['results']):  # for each single transcript in the IBM return dictionary
        for Words in SingleTranscript['alternatives'][0]['timestamps']:  # for each word in a given transcript
            SentenceCreated.append(Words[0])
            NewWord = np.array(FeatureExtractor(Words, sound_file))
            AllWords_Testing.append(NewWord)

    #for Word in range(len(AllWords_Testing)): #DEPRECIATED FOR NOW
        #for Row in range(len(AllWords_Testing[Word])):
            #AllWords_Testing[Word][Row][-1] = WordEncoder.fit_transform([AllWords_Testing[Word][Row][-1]])[0]

    AllWords_Testing = keras.preprocessing.sequence.pad_sequences(AllWords_Testing, maxlen = AllWords_Training.shape[1], dtype='object', padding = 'post')

    return AllWords_Testing, SentenceCreated





def FeatureExtractor(Words, sound_file): #extracts MFCC and word features from audio
    Word = Words[0]
    StartTime = Words[1] * 1000
    EndTime = Words[2] * 1000

    WantedAudio = sound_file[StartTime:EndTime]  # segment the audio file to include the word specified by the above for loop
    WantedAudio.export('Junk/audio_%s.wav' % Word)
    RATE_INPUT = WantedAudio.frame_rate
    SIG_INPUT = np.array(WantedAudio.get_array_of_samples())  # get rate and signal array from the segment

    ACCENT_MFCC_INPUT = librosa.feature.mfcc(y=SIG_INPUT, sr=RATE_INPUT, n_mfcc=20)  # get MFCC of the signal
    ACCENT_DELTA_INPUT = librosa.feature.delta(ACCENT_MFCC_INPUT, order=1)  # get delta of the signal
    ACCENT_DELTA_2_INPUT = librosa.feature.delta(ACCENT_MFCC_INPUT, order=2)  # get delta of the signal

    NewWord = pd.concat([pd.DataFrame(ACCENT_MFCC_INPUT).transpose(),
                         pd.DataFrame(ACCENT_DELTA_INPUT).transpose(),
                         pd.DataFrame(ACCENT_DELTA_2_INPUT).transpose(),
                         pd.DataFrame(Word,
                                      index=np.arange(0, len(ACCENT_MFCC_INPUT.transpose())),
                                      columns=np.arange(1))],
                        axis=1,
                        ignore_index=True)  # combine the array into a single dataframe including the MFCC, Delta, Word used to derive the MFCC/Delta, and the accent used

    return NewWord



def Load_Up():
    with open('AllWords_Training.pkl', 'rb') as f:
        AllWords_Training = pickle.load(f)
    with open('AllAccents_Training.pkl', 'rb') as f:
        AllAccents_Training = pickle.load(f)
    with open('WordEncoder.pkl', 'rb') as f:
        WordEncoder = pickle.load(f)
    with open('AccentEncoder.pkl', 'rb') as f:
        AccentEncoder = pickle.load(f)

    return AllWords_Training, AllAccents_Training, WordEncoder, AccentEncoder
