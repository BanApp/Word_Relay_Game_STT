from gtts import gTTS
import os
import speech_recognition as sr
import csv

f = open('myungsa.csv','r')
rdr = csv.reader(f)

def speak(text ,lang="ko", speed=False):
    tts = gTTS(text=text, lang=lang , slow=speed)
    tts.save("./tts.mp3")
    os.system("afplay " + "./tts.mp3")

Recognizer = sr.Recognizer()
mic = sr.Microphone()

tmp = []
p_key = 'a'
c_key = 'b'

with mic as source:
    audio = Recognizer.listen(source,timeout=5)

data = Recognizer.recognize_google(audio, language="ko")

ck = 0
for i in rdr:
    if i[0] == data and len(i[0]) > 1:
        p_key = data[-1]
        tmp.append(data)
        print("Player:",i[0])
        print('<pass>')
        ck = 1
        break

if ck == 0:
    print("규칙에 어긋납니다.")
    exit(0)

while 1:
    if ck == 1:
        f = open('myungsa.csv', 'r')
        rdr = csv.reader(f)

        for j in rdr:
            if (j[0][0] == p_key) and (len(j[0]) > 1) and (j[0] not in tmp):
                print("Computer:",j[0])
                print('<pass>')
                speak(j[0])
                tmp.append(j[0])
                c_key = j[0][-1]
                ck = 0
                break

    else:
        with mic as source:
            audio = Recognizer.listen(source, timeout=5)

        data = Recognizer.recognize_google(audio, language="ko")

        f = open('myungsa.csv', 'r')
        rdr = csv.reader(f)

        print("Player: ",data)
        ck = 2

        for i in rdr:
            if (i[0] == data) and (len(i[0]) > 1) and (data not in tmp) and (data[0] == c_key):
                p_key = data[-1]
                print('<pass>')
                ck = 1
                break

    if ck == 2:
        print('=========END========')
        print('====Computer WIN====')
        print('=====================')
        speak('Computer WIN')
        exit(0)