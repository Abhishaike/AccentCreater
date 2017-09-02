import json
from watson_developer_cloud import SpeechToTextV1
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.layers import LSTM
from keras.optimizers import RMSprop

IBM_USERNAME = USERNAME
IBM_PASSWORD =  PW
stt = SpeechToTextV1(username=IBM_USERNAME, password=IBM_PASSWORD)


scaler = StandardScaler()

TRAIN_DATA = np.array(AllWords_Training[AllWords_Training.columns[:-1]])
TRAIN_DATA_NORMALIZED = np.concatenate((scaler.fit_transform(TRAIN_DATA[:, :-1]), [[item] for item in TRAIN_DATA[:, -1]]), 1) #list comphrension used to make sub arrays out of a 1D array. This scales MFCC/Delta features, but not the word class
TRAIN_LABELS = np.array(AllWords_Training[AllWords_Training.columns[-1]])
TRAIN_LABELS.reshape((-1, 1))
TRAIN_LABELS = np_utils.to_categorical(TRAIN_LABELS) #turns this into a one-hot vector.

TEST_DATA = np.array(AllWords_Testing[AllWords_Testing.columns[:-1]])
TEST_DATA_NORMALIZED = np.concatenate((scaler.transform(TEST_DATA[:, :-1]), [[item] for item in TEST_DATA[:, -1]]), 1)
TEST_LABELS = np.array(AllWords_Testing[AllWords_Testing.columns[-1]])
TEST_LABELS.reshape((-1, 1))
TEST_LABELS = np_utils.to_categorical(TEST_LABELS)


###########
#DEEP NEURAL NET (MULTI-LAYER PERCEPTRON) MODEL

model = Sequential()
model.add(Dense(256, input_dim=61, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(5, activation='softmax'))
sgd = optimizers.SGD(lr=0.0005, momentum=.9)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
model.fit(TRAIN_DATA_NORMALIZED, TRAIN_LABELS, epochs=30, batch_size=500, validation_data = (TEST_DATA_NORMALIZED, TEST_LABELS), verbose = 2)

Predictions = model.predict(TEST_DATA_NORMALIZED)

for Label in Predictions:
    HighestIndices = np.argmax(Label)
    Label.fill(0)
    Label[HighestIndices] = 1

precision_score(TEST_LABELS, Predictions, average=None)

###############
#FRAME-BY-FRAME RECURRENT NEURAL NETWORK WITH LSTM CELLS 

TRAIN_DATA_NORMALIZED_1 = TRAIN_DATA_NORMALIZED
TRAIN_DATA_NORMALIZED_1 = np.reshape(TRAIN_DATA_NORMALIZED_1, (TRAIN_DATA_NORMALIZED_1.shape[0], 1, TRAIN_DATA_NORMALIZED_1.shape[1]))

TEST_DATA_NORMALIZED_1 = TEST_DATA_NORMALIZED
TEST_DATA_NORMALIZED_1 = np.reshape(TEST_DATA_NORMALIZED_1, (TEST_DATA_NORMALIZED_1.shape[0],1, TEST_DATA_NORMALIZED_1.shape[1]))


model = Sequential()
model.add(LSTM(512, activation='sigmoid', inner_activation='tanh',  input_shape=(1, 61), return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(512, activation='sigmoid', inner_activation='tanh', return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(512, activation='tanh', inner_activation='sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(5, activation='softmax'))
rms = keras.optimizers.RMSprop(lr=0.0001)
model.compile(loss='categorical_crossentropy', optimizer=rms, metrics=['accuracy'])
model.fit(TRAIN_DATA_NORMALIZED_1, TRAIN_LABELS, epochs=30, batch_size=100, verbose = 2, validation_data = (TEST_DATA_NORMALIZED_1, TEST_LABELS))

Predictions = model.predict(TEST_DATA_NORMALIZED_1)

for Label in Predictions:
    HighestIndices = np.argmax(Label)
    Label.fill(0)
    Label[HighestIndices] = 1

precision_score(TEST_LABELS, Predictions, average=None)

#############
