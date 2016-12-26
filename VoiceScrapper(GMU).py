IndianCombined = AudioSegment.empty()
for x in INDIAN:
	page = urllib.urlopen(x, 'lxml')
	html = page.read()
	soup = BeautifulSoup(html)
	x = soup.audio.source
	y = x.get('src')
	urllib.urlretrieve (y, "TESTER/INDIAN/INDIAN.mp3")
	AudioSegment.from_mp3("TESTER/INDIAN/INDIAN.mp3").export("TESTER/INDIAN/INDIAN.wav", format="wav")
	sound = AudioSegment.from_file("TESTER/INDIAN/INDIAN.wav")
	IndianCombined += sound

IndianCombined.export("TESTER/INDIAN/INDIAN.wav", format='wav')


AmericanCombined = AudioSegment.empty()
for x in AMERICAN:
	page = urllib.urlopen(x, 'lxml')
	html = page.read()
	soup = BeautifulSoup(html)
	x = soup.audio.source
	y = x.get('src')
	urllib.urlretrieve (y, "TESTER/AMERICAN/AMERICAN.mp3")
	AudioSegment.from_mp3("TESTER/AMERICAN/AMERICAN.mp3").export("TESTER/AMERICAN/AMERICAN.wav", format="wav")
	sound = AudioSegment.from_file("TESTER/AMERICAN/AMERICAN.wav")
	AmericanCombined += sound

AmericanCombined.export("TESTER/AMERICAN/AMERICAN.wav", format='wav')


AustralianCombined = AudioSegment.empty()
for x in AUSTRALIAN:
	page = urllib.urlopen(x, 'lxml')
	html = page.read()
	soup = BeautifulSoup(html)
	x = soup.audio.source
	y = x.get('src')
	urllib.urlretrieve (y, "TESTER/AUSTRALIAN/AUSTRALIAN.mp3")
	AudioSegment.from_mp3("TESTER/AUSTRALIAN/AUSTRALIAN.mp3").export("TESTER/AUSTRALIAN/AUSTRALIAN.wav", format="wav")
	sound = AudioSegment.from_file("TESTER/AUSTRALIAN/AUSTRALIAN.wav")
	AustralianCombined += sound

AustralianCombined.export("TESTER/AUSTRALIAN/AUSTRALIAN.wav", format='wav')
