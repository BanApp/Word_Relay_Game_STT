import sys
import pandas as pd
from gtts import gTTS
import os
import speech_recognition as sr
import random

def speak(text ,lang="ko", speed=False):
    tts = gTTS(text=text, lang=lang , slow=speed)
    tts.save("./tts.mp3")
    os.system("afplay " + "./tts.mp3")


def etoe(time,level):
    rdr = pd.read_csv('myungsa.csv', engine='pyarrow', index_col=0)

    Recognizer = sr.Recognizer()
    mic = sr.Microphone()

    tmp = []
    check = {}
    p_key = 'a'
    c_key = 'b'

    with mic as source:
        audio = Recognizer.record(source, duration=time)

    try:
        data = Recognizer.recognize_google(audio_data=audio, language="ko-kr")
        print("Player: ", data)
    except sr.UnknownValueError:
        print("Your speech can not understand")
    except sr.RequestError as e:
        print("Request Error!; {0}".format(e))

    # data = sys.stdin.readline().rstrip() #텍스트 직접 입력

    ck = 0
    for i in rdr.index:
        if i == data and len(i) > 1:
            p_key = data[-1]
            tmp.append(data)
            print("Player:", i)
            print('<pass>')
            ck = 1
            break

    if ck == 0:
        print("한글자 단어는 사용할 수 없습니다. 규칙에 어긋납니다.")
        speak("한글자 단어는 사용할 수 없습니다. 규칙에 어긋납니다.")
        exit(0)

    while 1:
        if ck == 1:
            # 컴퓨터 순서
            ck = 3
            rd = []
            for j in rdr.index:
                if (j[0] == p_key) and (len(j) > 1) and (j not in tmp):
                    rd.append(j)

            x = random.choice(rd)
            if x[0] not in check:
                check[x[0]] = 1
            else:
                check[x[0]] += 1

            if check[x[0]] <= level:
                print("Computer:", x)
                print('<pass>')
                speak(x)
                tmp.append(x)
                c_key = x[-1]
                ck = 0
            else:
                ck = 3

        elif ck == 0:
            # 사람 순서
            with mic as source:
                audio = Recognizer.record(source, duration=time)
            try:
                data = Recognizer.recognize_google(audio_data=audio, language="ko-kr")
                print("Player: ", data)
            except sr.UnknownValueError:
                print("Your speech can not understand")
            except sr.RequestError as e:
                print("Request Error!; {0}".format(e))

            # data = sys.stdin.readline().rstrip() #텍스트 직접 입력

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
            print('=========END=========')
            print('======Human WIN======')
            print('======================')
            speak('Human WIN')
            exit(0)

print("지속 시간과 난이도를 입력해주세요:")
x,y = map(int,sys.stdin.readline().split())
etoe(x,y)
