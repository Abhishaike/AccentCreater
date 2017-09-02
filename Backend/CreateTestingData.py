def CreateTestingData():
    AllWords_Testing = pd.DataFrame()
    AllWords_Training = pd.DataFrame()
    for AccentInfo, AccentName in [(AMERICAN, "AMERICAN"),
                                   (INDIAN, "INDIAN"),
                                   (AUSTRALIAN, "AUSTRALIAN"),
                                   (MANDARIN, "MANDARIN"),
                                   (RUSSIAN, "RUSSIAN")]: #these tuples represent all the accents being tested/trained
        AccentInfo_Train, AccentInfo_Test = train_test_split(AccentInfo, test_size = 0.2, random_state = 42) #split links into a training and testing sset.
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
                    Word = Words[0]
                    StartTime = Words[1] * 1000
                    EndTime = Words[2] * 1000

                    WantedAudio = sound_file[StartTime:EndTime] #segment the audio file to include the word specified by the above for loop
                    RATE_INPUT = WantedAudio.frame_rate
                    SIG_INPUT = np.array(WantedAudio.get_array_of_samples()) #get rate and signal array from the segment

                    ACCENT_MFCC_INPUT = librosa.feature.mfcc(y = SIG_INPUT, sr = RATE_INPUT, n_mfcc=20) #get MFCC of the signal
                    ACCENT_DELTA_INPUT = librosa.feature.delta(ACCENT_MFCC_INPUT, order = 1) #get delta of the signal
                    ACCENT_DELTA_2_INPUT = librosa.feature.delta(ACCENT_MFCC_INPUT, order = 2) #get delta of the signal

                    NewWord = pd.concat([pd.DataFrame(ACCENT_MFCC_INPUT).transpose(),
                                         pd.DataFrame(ACCENT_DELTA_INPUT).transpose(),
                                         pd.DataFrame(ACCENT_DELTA_2_INPUT).transpose(),
                                         pd.DataFrame(Word,
                                                      index=np.arange(0, len(ACCENT_MFCC_INPUT.transpose())),
                                                      columns=np.arange(1)),
                                         pd.DataFrame(AccentName,
                                                      index=np.arange(0, len(ACCENT_MFCC_INPUT.transpose())),
                                                      columns=np.arange(1))],
                                        axis = 1, ignore_index = True) #combine the array into a single dataframe including the MFCC, Delta, Word used to derive the MFCC/Delta, and the accent used

                    if PersonLink in AccentInfo_Train: #if the link is part of training links, save it to AllWords_Training. Else, save it to AllWords_Testing
                        AllWords_Training = pd.concat([AllWords_Training,
                                                      NewWord],
                                             axis = 0, ignore_index = True)
                    else:
                        AllWords_Testing = pd.concat([AllWords_Testing,
                                                    NewWord],
                                             axis = 0, ignore_index = True)

                    AllWords_Testing.reset_index(drop = True, inplace=True)
                    AllWords_Training.reset_index(drop = True, inplace=True)

    AllWords_Testing.columns = [i for i in range(AllWords_Testing.shape[1])]
    AllWords_Training.columns = [i for i in range(AllWords_Training.shape[1])]

    WordEncoder = LabelEncoder().fit(AllWords_Training[AllWords_Training.columns[-2]].append(AllWords_Testing[AllWords_Testing.columns[-2]],ignore_index=True)) #turns all unique words into 'classes'
    AllWords_Training[AllWords_Training.columns[-2]] = pd.DataFrame(WordEncoder.transform(AllWords_Training[AllWords_Training.columns[-2]]))
    AllWords_Testing[AllWords_Testing.columns[-2]] = pd.DataFrame(WordEncoder.transform(AllWords_Testing[AllWords_Testing.columns[-2]]))


    AccentEncoder = LabelEncoder().fit(AllWords_Training[AllWords_Training.columns[-1]].append(AllWords_Testing[AllWords_Testing.columns[-1]],ignore_index=True)) #turns all unique accents into 'classes'
    AllWords_Training[AllWords_Training.columns[-1]] = pd.DataFrame(AccentEncoder.transform(AllWords_Training[AllWords_Training.columns[-1]]))
    AllWords_Testing[AllWords_Testing.columns[-1]] = pd.DataFrame(AccentEncoder.transform(AllWords_Testing[AllWords_Testing.columns[-1]]))




AMERICAN = ["http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=61",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=110",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=132",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=73",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=74",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=76",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=81",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=83",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=84",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=92",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=95",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=105",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=106",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=109",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=112",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=114",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=120",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=122",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=124",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=125",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=199",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=198",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2286",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2350",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=265"]

INDIAN =    ["http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=207",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=587",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=593",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=910",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1017",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1437",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1697",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1966",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2209",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2236",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2242",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2303",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2353",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2354",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2356",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2366"]

AUSTRALIAN = ["http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=131",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=136",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=140",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=148",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=485",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=525",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=529",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=533",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=776",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=961",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1072",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1085",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1352",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1377",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1547",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1733",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2104",
              "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2172"]


MANDARIN = ["http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=258",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=430",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=451",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=491",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=719",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=796",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=916",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1154",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1447",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1490",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1541",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1614",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1630",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1645",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1736",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1792",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1990",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2117",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2119",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2274",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2281",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2282",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2323",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2348"]


RUSSIAN = [ "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=299",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=308",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=309",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=301",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=460",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=472",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=609",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=648",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=671",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=831",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=834",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=994",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1191",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1254",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1279",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1311",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1407",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1467",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1518",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1523",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=1708",
            "http://accent.gmu.edu/searchsaa.php?function=detail&speakerid=2369"]
