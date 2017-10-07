from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
from watson_developer_cloud import SpeechToTextV1
from pydub import AudioSegment
import numpy as np
import os
import h5py

# set ffmpeg location for AudioSegment
AudioSegment.converter = "ffmpeg/ffmpeg"

# get IBM credentials
IBM_USERNAME = os.environ.get("IBM_USERNAME", None)
IBM_PASSWORD = os.environ.get("IBM_PASSWORD", None)
if IBM_USERNAME is None or IBM_USERNAME is None:
    raise Exception("Could not find IBM info")
    
def main(FILEPATH): #currently, WordEncoder is depreciated due to shitty the shitty sklearn LabelEncoder technique; unique words in testing data cause errors
    if not os.path.exists('LSTM_MODEL_ARCHITECTURE_WEIGHTS.h5'): #if model doesnt exist, get the model created and trained
        raise Exception("couldn't find the model")

    model = load_model('LSTM_MODEL_ARCHITECTURE_WEIGHTS.h5')
    AllWords_Training, AllAccents_Training, WordEncoder, AccentEncoder = Load_Up(Accent_Encoder = True) #loads all of these variables from the pickled files, by default, only AccentEncoder is returned
    AllWords_Testing, SentenceCreated = CreateTestingData(FILEPATH, model) #creates testing data from the previous
    AllPredictions_Word = Test(AllWords_Testing, SentenceCreated, AccentEncoder, model) #predicts accent labels for all testing data, and return a tuple of (word, array_of_predictions_per_accent)
    return AllPredictions_Word

def Load_Up(Words = False, Accent = False, Word_Encoder = False, Accent_Encoder = False):
    if Words:
        with open('AllWords_Training.pkl', 'rb') as f:
            AllWords_Training = pickle.load(f)
    else:
        AllWords_Training = 0

    if Accent:
        with open('AllAccents_Training.pkl', 'rb') as f:
            AllAccents_Training = pickle.load(f)
    else:
        AllAccents_Training = 0

    if Word_Encoder:
        with open('WordEncoder.pkl', 'rb') as f:
            WordEncoder = pickle.load(f)
    else:
        WordEncoder = 0

    if Accent_Encoder:
        with open('AccentEncoder.pkl', 'rb') as f:
            AccentEncoder = pickle.load(f)
    else:
        AccentEncoder = 0

    return AllWords_Training, AllAccents_Training, WordEncoder, AccentEncoder

def CreateTestingData(FILEPATH, model):
    global IBM_USERNAME
    global IBM_PASSWORD
    stt = SpeechToTextV1(username=IBM_USERNAME, password=IBM_PASSWORD)
    AllWords_Testing = []
    SentenceCreated = []
    AudioSegment.from_file(FILEPATH, "3gp").export("test1.wav",format="wav")  # open link, save it to a dummy .mp3 file, convert to .wav, and get audiosegment of it
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

    AllWords_Testing = pad_sequences(AllWords_Testing, maxlen = model._flattened_layers[0].batch_input_shape[1], dtype='object', padding = 'post')

    return AllWords_Testing, SentenceCreated

def Test(AllWords_Testing, SentenceCreated, AccentEncoder, model):
    AllPredictions_NoWord = []
    AllWords_Testing = np.delete(AllWords_Testing, np.s_[-1], axis=2)
    for Word, WordData in enumerate(AllWords_Testing):
        Predictions =  model.predict(np.reshape(WordData,(1, WordData.shape[0], WordData.shape[1])))
        AllPredictions_NoWord.append(list(zip(AccentEncoder.classes_, Predictions[0])))

    AllPredictions_Word = list(zip(SentenceCreated, AllPredictions_NoWord))
    return AllPredictions_Word