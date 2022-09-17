import sys
import pandas as pd
from gtts import gTTS
import os
import speech_recognition as sr
import random

rdr = pd.read_csv('myungsa.csv',engine='pyarrow',index_col=0)
def speak(text ,lang="ko", speed=False):
    tts = gTTS(text=text, lang=lang , slow=speed)
    tts.save("./tts.mp3")
    os.system("afplay " + "./tts.mp3")

Recognizer = sr.Recognizer()
mic = sr.Microphone()

tmp = []
check = {}
p_key = 'a'
c_key = 'b'

#with mic as source:
    #audio = Recognizer.listen(source,timeout=5)

#data = Recognizer.recognize_google(audio_data=audio, language="ko-kr")

data = sys.stdin.readline().rstrip() #텍스트 직접 입력

ck = 0
for i in rdr.index:
    if i == data and len(i) > 1:
        p_key = data[-1]
        tmp.append(data)
        print("Player:",i)
        print('<pass>')
        ck = 1
        break

if ck == 0:
    print("규칙에 어긋납니다.")
    exit(0)

while 1:
    if ck == 1:
        #컴퓨터 순서
        ck = 3
        rd = []
        for j in rdr.index:
            if (j[0] == p_key) and (len(j) > 1) and (j not in tmp):
                rd.append(j)
            if len(rd) > 4:
                x = random.choice(rd)
                if x[0] not in check:
                    check[x[0]] = 1
                else:
                    check[x[0]] += 1

                if check[x[0]] <= 2:
                    print("Computer:", x)
                    print('<pass>')
                    speak(x)
                    tmp.append(x)
                    c_key = x[-1]
                    ck = 0
                    break
                else:
                    ck = 3
                    break

    elif ck == 0:
        #사람 순서
        #with mic as source:
            #audio = Recognizer.listen(source, timeout=5)
        #data = Recognizer.recognize_google(audio_data=audio, language="ko-kr")

        data = sys.stdin.readline().rstrip() #텍스트 직접 입력
        print("Player: ",data)
        ck = 2
        for i in rdr.index:
            if (i == data) and (len(i) > 1) and (data not in tmp) and (data[0] == c_key):
                p_key = data[-1]
                print('<pass>')
                ck = 1
                break

    elif ck == 2:
        print('=========END========')
        print('====Computer WIN====')
        print('=====================')
        speak('Computer WIN')
        exit(0)

    elif ck == 3:
        print('=========END========')
        print('====Human WIN====')
        print('=====================')
        speak('Human WIN')
        exit(0)

