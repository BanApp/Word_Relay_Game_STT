import sys
import tkinter.messagebox
import pandas as pd
from gtts import gTTS
import speech_recognition as sr
import random
import time
import os
import threading
from tkinter import *
import tkinter.font as tkFont
global audio
import tkinter.ttk as ttk

#tkinter 시작
window = Tk()

window.title("Word Relay Game")
window.geometry("540x600")
window.resizable(False, False)

fontStyle = tkFont.Font(family="Lucida Grande", size=30)
s_fontStyle = tkFont.Font(family="Lucida Grande", size=15)

#음성인식
def rec(s,t):
    global audio
    Recognizer = sr.Recognizer()
    audio = Recognizer.record(s, duration=t)

#컴퓨터 소리 출력
def speak(text ,lang="ko", speed=False):
    tts = gTTS(text=text, lang=lang , slow=speed)
    tts.save("./tts.mp3")
    os.system("afplay " + "./tts.mp3")

#끝말잇기 게임
def etoe(time,level,name):
    global audio
    rdr = pd.read_csv('myungsa.csv', engine='pyarrow', index_col=0)
    Recognizer = sr.Recognizer()
    mic = sr.Microphone()
    tmp = []
    check = {}
    p_key = 'a'
    c_key = 'b'
    ck = 1

    while 1:
        with mic as source:
            rec(source,time)
        try:
            data = Recognizer.recognize_google(audio_data=audio, language="ko-kr")
            data = data.replace(" ", "")

            msg = tkinter.messagebox.askyesno("확인","입력한 데이터가 "+ str(data) + " 맞습니까?")

            print(name, ": ", data)

            if msg == True:
                label_pname = Label(window, font=fontStyle)
                label_pname.configure(text=str(name) + ": ")
                label_pname.place(x=110, y=350)

                label_pdata = Label(window, font=fontStyle)
                label_pdata.configure(text=str(data))
                label_pdata.place(x=300, y=350)
                window.update()
                break

            else:
                tkinter.messagebox.askretrycancel(title="재시도",message="Retry 버튼을 누르고 다시 말씀하세요!")
                continue

        except sr.UnknownValueError:
            tkinter.messagebox.showwarning(title="시간초과",message="시간초과 입니다!")
            speak("시간초과 입니다.")
            ck=2
            break

        except sr.RequestError as e:
            print("Request Error!; {0}".format(e))
            break

    # data = sys.stdin.readline().rstrip() #텍스트 직접 입력

    while 1:
        if ck != 2:
            for i in rdr.index:
                i = i.replace(" ", "")
                if i == data and len(i) > 1:
                    p_key = data[-1]
                    tmp.append(data)
                    print()
                    ck = 1
                    break

        if ck == 0:
            tkinter.messagebox.showerror(title="규칙위반", message="규칙에 어긋납니다.")
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

                if len(rd) == 0:
                    tkinter.messagebox.showerror(title="규칙위반", message="규칙에 어긋납니다.")
                    speak("규칙에 어긋납니다.")
                    exit(0)

                x = random.choice(rd)
                if x[0] not in check:
                    check[x[0]] = 1
                else:
                    check[x[0]] += 1

                if check[x[0]] <= level:
                    label_cname = Label(window,font=fontStyle)
                    label_cname.configure(text="Computer: ")
                    label_cname.place(x=110, y=420)

                    label_cdata = Label(window,font=fontStyle)
                    label_cdata.configure(text=str(x))
                    label_cdata.place(x=300, y=420)
                    window.update()
                    print("Computer:", x)
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
                        rec(source,time)

                    try:
                        data = Recognizer.recognize_google(audio_data=audio, language="ko-kr")
                        data = data.replace(" ", "")
                        pmsg = tkinter.messagebox.askyesno("확인", "입력한 데이터가 " + str(data) + " 맞습니까?")

                        if pmsg == True:
                            label_cdata.destroy()
                            label_cname.destroy()

                            label_pname.destroy()
                            label_pdata.destroy()

                            label_pname = Label(window,font=fontStyle)
                            label_pname.configure(text=str(name) + ": ")
                            label_pname.place(x=110, y=350)

                            label_pdata = Label(window,font=fontStyle)
                            label_pdata.configure(text=str(data))
                            label_pdata.place(x=300, y=350)
                            print(name, ": ", data)
                            window.update()
                            break

                        elif pmsg == False:
                            tkinter.messagebox.askretrycancel(title="재시도", message="Retry 버튼을 누르고 다시 말씀하세요!")
                            continue

                    except sr.UnknownValueError:
                        print("시간초과 입니다.")
                        speak("시간초과 입니다.")
                        ck = 2
                        break

                    except sr.RequestError as e:
                        print("Request Error!; {0}".format(e))
                        break

                # data = sys.stdin.readline().rstrip() #텍스트 직접 입력

                ck = 2
                for i in rdr.index:
                    if (i == data) and (len(i) > 1) and (data not in tmp) and (data[0] == c_key):
                        p_key = data[-1]
                        # print('[Pass]')
                        print()
                        ck = 1
                        break

            elif ck == 2:
                # 컴퓨터 승리
                speak('Computer WIN')
                tkinter.messagebox.showinfo(title="컴퓨터 승리", message="컴퓨터가 승리했습니다! 다음번엔 이겨봅시다!")
                exit(0)

            elif ck == 3:
                # 사람 승리
                speak(name + 'WIN')
                tkinter.messagebox.showinfo(title=name + " 승리", message=name + " 승리! 축하합니다!")
                exit(0)

def start():
    def btncmd():
        name = e.get()
        x = combobox_t.get()
        y = combobox_l.get()

        if y == "쉬움":
            y = 1
        elif y == "보통":
            y = 2
        else:
            y = 3
        etoe(int(x[0]), int(y), name)

    label_s = Label(window,font=tkFont.Font(family="Lucida Grande", size=18))
    label_s.configure(text="표준국어대사전 기반 끝말잇기 게임 (단국대학교 컴퓨터공학과 정민준)")
    label_s.place(x=5, y=15)

    label_user = Label(window,font=s_fontStyle)
    label_user.configure(text="유저의 닉네임을 입력해주세요: ")
    label_user.place(x=5, y=80)

    e = Entry(window, width=20)
    e.place(x=210, y=80)
    e.insert(0, '')

    label_t = Label(window,font=s_fontStyle)
    label_t.configure(text="음성 인식 지속 시간을 선택해주세요: ")
    label_t.place(x=5, y=130)

    a = ["1초","2초","3초","4초","5초","6초","7초","8초","9초","10초"]  # 콤보 박스에 나타낼 항목 리스트
    combobox_t = ttk.Combobox(window)
    combobox_t.config(height=5)  # 높이 설정
    combobox_t.config(values=a)
    combobox_t.config(state="readonly")
    combobox_t.set("5초")  # 맨 처음 나타낼 값 설정
    combobox_t.place(x=280, y=130)

    label_level = Label(window,font=s_fontStyle)
    label_level.configure(text="끝말잇기의 난이도를 선택 해주세요: ")
    label_level.place(x=5, y=180)

    b = ['쉬움','보통','어려움']
    combobox_l = ttk.Combobox(window)
    combobox_l.config(height=5)  # 높이 설정
    combobox_l.config(values=b)
    combobox_l.config(state="readonly")
    combobox_l.set("쉬움")  # 맨 처음 나타낼 값 설정
    combobox_l.place(x=280, y=180)

    btn = Button(window, text="시작", command=btncmd,width=4,height=1,font=('koverwatch',40),fg ="green")
    btn.place(x=200, y=250)

start()

window.mainloop()
#tkinter 종료