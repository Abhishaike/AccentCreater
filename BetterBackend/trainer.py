from watson_developer_cloud import SpeechToTextV1
from bs4 import BeautifulSoup
import urllib
from pydub import AudioSegment
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle
from keras.preprocessing.sequence import pad_sequences
from keras.optimizers import RMSprop
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential

# urlopen compatibility w python2 and python3
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

def main(FILEPATH):
    if not os.path.exists('LSTM_MODEL_ARCHITECTURE_WEIGHTS.h5'): #if model doesnt exist, get the model created and trained
        AllWords_Training, AllAccents_Training, WordEncoder, AccentEncoder = CreateTrainingData()
        Train_and_Pickle_NN(AllWords_Training, AllAccents_Training)
        return "Didn't have required files, good to go now."

def CreateTrainingData():
    global IBM_USERNAME
    global IBM_PASSWORD
    stt = SpeechToTextV1(username=IBM_USERNAME, password=IBM_PASSWORD)
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

    AllWords_Training = pad_sequences(AllWords_Training, dtype='object', padding = 'pre')
    AllWords_Training = np.delete(AllWords_Training, np.s_[-1], axis=2)

    AllAccents_Training.reshape((-1, 1))
    AllAccents_Training = np_utils.to_categorical(AllAccents_Training)  # turns this into a one-hot vector.

    with open('AllWords_Training.pkl', 'wb') as f:
        pickle.dump(AllWords_Training, f, protocol=2)
    with open('AllAccents_Training.pkl', 'wb') as f:
        pickle.dump(AllAccents_Training, f, protocol=2)
    with open('WordEncoder.pkl', 'wb') as f:
        pickle.dump(WordEncoder, f, protocol=2)
    with open('AccentEncoder.pkl', 'wb') as f:
        pickle.dump(AccentEncoder, f, protocol=2)

    return AllWords_Training, AllAccents_Training, WordEncoder, AccentEncoder

def Train_and_Pickle_NN(AllWords_Training, AllAccents_Training) :
    #X_train, X_test, y_train, y_test = train_test_split(AllWords_Training, AllAccents_Training, test_size = 0.10, random_state = 41, stratify = AllAccents_Training)
    model = Sequential()
    model.add(LSTM(256, activation='tanh',recurrent_activation='sigmoid', stateful=False, return_sequences=True, input_shape=(AllWords_Training.shape[1], AllWords_Training.shape[2])))
    model.add(Dropout(.7))
    model.add(LSTM(256, activation='tanh',recurrent_activation='sigmoid', return_sequences=True))
    model.add(Dropout(.7))
    model.add(LSTM(256, activation='tanh',recurrent_activation='sigmoid', return_sequences=False))  # false because we want prediction per sequence, not per time-step
    model.add(Dropout(.7))
    model.add(Dense(5, activation='softmax'))
    rms = RMSprop(lr=0.001)
    model.compile(loss='categorical_crossentropy', optimizer=rms, metrics=['accuracy'])
    model.fit(AllWords_Training, AllAccents_Training, epochs = 30, batch_size=200, verbose=2)
    #model.fit(X_train, y_train, epochs = 40, batch_size=200, verbose=2, validation_data = (X_test, y_test))

    #model.save('LSTM_MODEL_ARCHITECTURE_WEIGHTS.h5')
    #Preds = []
    #Truth = []
    #for item in range(len(x)):
        #HighestIndices_Pred = np.argmax(x[item])
        #HighestIndices_Truth = np.argmax(y_test[item])
        #Preds.append(HighestIndices_Pred)
        #Truth.append(HighestIndices_Truth)