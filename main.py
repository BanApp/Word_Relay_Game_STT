import sys
import pandas as pd
from gtts import gTTS
import os
import speech_recognition as sr
import random
import time
import os
from tkinter import *


def countdown(num_of_secs):
    while num_of_secs:
        s = num_of_secs
        print(s, end=' ')
        time.sleep(1)
        num_of_secs -= 1
    print('시간종료')

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
    k = 'Y'
    while 1:
        with mic as source:
            audio = Recognizer.record(source, duration=time)
        try:
            data = Recognizer.recognize_google(audio_data=audio, language="ko-kr")
            data = data.replace(" ", "")
            print("Player: ",data)
            print('[Y/N]')

            k = sys.stdin.readline().rstrip()

            if k == 'Y':
                break
            else:
                print("다시 한번 말씀하세요!")

        except sr.UnknownValueError:
            print("시간초과 입니다.")
            speak("시간초과 입니다.")
            break

        except sr.RequestError as e:
            print("Request Error!; {0}".format(e))
            break

    # data = sys.stdin.readline().rstrip() #텍스트 직접 입력

    ck = 0
    for i in rdr.index:
        i = i.replace(" ", "")
        if i == data and len(i) > 1:
            p_key = data[-1]
            tmp.append(data)
            print('[Pass]')
            print()
            ck = 1
            break

    if ck == 0:
        print("규칙에 어긋납니다.")
        speak("규칙에 어긋납니다.")
        exit(0)

    while 1:
        if ck == 1:
            # 컴퓨터 순서
            ck = 3
            rd = []
            for j in rdr.index:
                j = j.replace(" ", "")
                if (j[0] == p_key) and (len(j) > 1) and (j not in tmp):
                    rd.append(j)

            x = random.choice(rd)
            if x[0] not in check:
                check[x[0]] = 1
            else:
                check[x[0]] += 1

            if check[x[0]] <= level:
                print("Computer:", x)
                print('[Pass]')
                print()
                speak(x)
                tmp.append(x)
                c_key = x[-1]
                ck = 0
            else:
                ck = 3

        elif ck == 0:
            # 사람 순서
            while 1:
                with mic as source:
                    audio = Recognizer.record(source, duration=time)
                try:
                    data = Recognizer.recognize_google(audio_data=audio, language="ko-kr")
                    data = data.replace(" ", "")
                    print("Player: ", data)
                    print('[Y/N]')
                    k = sys.stdin.readline().rstrip()

                    if k == 'Y':
                        break
                    else:
                        print("다시 한번 말씀하세요!")

                except sr.UnknownValueError:
                    print("시간초과 입니다.")
                    speak("시간초과 입니다.")
                    break

                except sr.RequestError as e:
                    print("Request Error!; {0}".format(e))
                    break

            # data = sys.stdin.readline().rstrip() #텍스트 직접 입력

            ck = 2
            for i in rdr.index:
                if (i == data) and (len(i) > 1) and (data not in tmp) and (data[0] == c_key):
                    p_key = data[-1]
                    print('[Pass]')
                    print()
                    ck = 1
                    break

        elif ck == 2:
            #컴퓨터 승리
            print('=========END========')
            print('====Computer WIN====')
            print('=====================')
            speak('Computer WIN')
            print("다시 하시겠습니까?[Y/N]")
            p = sys.stdin.readline().rstrip()
            if p == 'Y':
                return 1
            else:
                print('프로그램을 종료 합니다.')
                exit(0)

        elif ck == 3:
            #사람 승리
            print('=========END=========')
            print('======Human WIN======')
            print('======================')
            speak('Human WIN')
            print("다시 하시겠습니까?[Y/N]")
            p = sys.stdin.readline().rstrip()
            if p == 'Y':
                return 1
            else:
                print('프로그램을 종료 합니다.')
                exit(0)

def first():
    while 1:
        print("<음성 인식 지속 시간과 난이도를 입력해주세요>")
        x, y = map(int, sys.stdin.readline().split())
        etoe(x,y)

first()

