from tkinter import *
from tkinter.ttk import *
import os
from tkinter.ttk import Style as Style_
from tkinter import LEFT, TOP, X, FLAT, RAISED
from PIL import Image, ImageTk
from tkinter import filedialog as fd


def contador():

    global play
    global segundos
    global minutos
    global home_score
    global away_score

    if play:

        s = ''
        m = ''

        if (segundos > 59):
            minutos += 1
            segundos = 0

        if (segundos < 10):
            s = '0'

        if (minutos < 10):
            m = '0'

        m_ = m + str(minutos)
        s_ = s + str(segundos)
        time_ = m_ + ':' + s_

        setOutput('time', time_)
        lbl_time.config(text=time_)
        txt_time.delete(0, END)
        txt_time.insert(0, time_)
        root.after(1000, contador)
        segundos += 1


def toggle():
    global etiqueta
    global play
    global visita
    play = not play

    filetypes = [('Image files', '.jpg .jpeg .png')]

    filename = fd.askopenfilename(
        title='Open a file', initialdir='/', filetypes=filetypes)

    if play:
        img_path = "assets/pause.png"
        txt_time.place_forget()
        lbl_time.place(x=498, y=76)
        # lbl_time.config(borderwidth=1, relief=SOLID, padding=7)
        btn_time_minutes_add.config(state=DISABLED)
        btn_time_minutes_substract.config(state=DISABLED)
        btn_time_seconds_add.config(state=DISABLED)
        btn_time_seconds_substract.config(state=DISABLED)
    else:
        img_path = "assets/play.png"
        txt_time.place(x=490, y=75)
        lbl_time.place_forget()
        btn_time_minutes_add.config(state=WRITABLE)
        btn_time_minutes_substract.config(state=WRITABLE)
        btn_time_seconds_add.config(state=WRITABLE)
        btn_time_seconds_substract.config(state=WRITABLE)

    if (os.path.exists(img_path)):
        img = Image.open(img_path)
        eimg = ImageTk.PhotoImage(img)
        btn_play.config(image=eimg)
        btn_play.image_names = eimg

    contador()


def restart():
    global segundos
    global minutos
    global home_score
    global away_score

    segundos = 0
    minutos = 0
    home_score = 0
    away_score = 0
    setOutput('00:00', 'time')
    spn_home_score.set(home_score)
    spn_away_score.set(away_score)


def setOutput(target, value):
    global path

    try:
        if not os.path.isdir(path):
            os.mkdir(path)
    except OSError as error:
        print(error)

    with open(path + '/' + target + '.txt', 'w') as f:
        try:
            f.write(str(value).upper())
        except OSError as error:
            print(error)


def callback(sv, prefijo):
    setOutput(sv.get(), prefijo)


def setTime(v):

    global minutos
    global segundos


def on_focus_out(event):
    global minutos
    global segundos

    if play == False:
        if event.widget == txt_time:
            value = txt_time.get()
            if (value):
                tmp = value.split(':')
                if len(tmp) == 2:
                    if not tmp[0].isnumeric():
                        tmp[0] = 0
                    if not tmp[1].isnumeric():
                        tmp[1] = 0

                    minutos = int(tmp[0])
                    segundos = int(tmp[1])
                else:
                    minutos = 0
                    segundos = 0
                    time_ = '00:00'

                s_ = str(segundos)
                s_ = s_.zfill(2)
                m_ = str(minutos)
                m_ = m_.zfill(2)
                time_ = m_ + ':' + s_

                setOutput('time', time_)
                txt_time.delete(0, END)
                txt_time.insert(0, time_)
                lbl_time.config(text=time_)
            else:
                minutos = 0
                segundos = 0
                time_ = '00:00'
                setOutput('time', time_)
                txt_time.delete(0, END)
                txt_time.insert(0, time_)
                lbl_time.config(text=time_)

    if event.widget == txt_home_name:
        setOutput('home_name', txt_home_name.get())
    elif event.widget == txt_away_name:
        setOutput('away_name', txt_away_name.get())


def setScore(v):
    txt = ''
    if v == 'home_score':
        txt = spn_home_score.get()
    else:
        txt = spn_away_score.get()

    setOutput(txt, v)


def scoreUpdate(target, value):
    global home_score
    global away_score
    score = 0

    if target == 'home_score':
        home_score += value

        if home_score < 0:
            home_score = 0

        txt_home_score.delete(0, END)
        txt_home_score.insert(0, str(home_score))
        score = home_score

    if target == 'away_score':
        away_score += value

        if away_score < 0:
            away_score = 0

        txt_away_score.delete(0, END)
        txt_away_score.insert(0, str(away_score))
        score = away_score

    setOutput(target, score)


def timeUpdate(target, value):

    global play
    global segundos
    global minutos
    global home_score
    global away_score

    if not play:
        s = ''
        m = ''

        if target == 'segundos':
            segundos += value

            if segundos > 59:
                minutos += 1
                segundos = 0

            if segundos < 0:
                if minutos >= 1:
                    segundos = 59
                    minutos -= 1
                else:
                    segundos = 0

        if target == 'minutos':
            minutos += value

            if minutos < 0:
                minutos = 0

        if (segundos < 10):
            s = '0'

        if (minutos < 10):
            m = '0'

        m_ = m + str(minutos)
        s_ = s + str(segundos)
        time_ = m_ + ':' + s_
        setOutput('time', time_)
        lbl_time.config(text=time_)
        txt_time.delete(0, END)
        txt_time.insert(0, time_)


def getOutput(target):
    file = 'output/' + target + '.txt'
    response = ''
    if (os.path.exists(file)):
        f = open(file, 'r')
        response = f.read()

    return response


def setImage(widget, path):

    if (os.path.exists(path)):
        img = Image.open(path)
        eimg = ImageTk.PhotoImage(img)
        widget.config(image=eimg)
        widget.image_names = eimg


version = "v0.1"  # 2024-04-24
root = Tk()
root.geometry("800x200")
root.title("Scoreboard MX " + version + " - El Juego Perfecto MX")
root.resizable(False, False)

img = "assets/icon.ico"
if (os.path.exists(img)):
    root.iconbitmap(img)

global path
global etiqueta
global home_name
global home_score
global play

play = False

path = "output"
etiqueta = "Start"

home_name = getOutput('home_name')
if home_name == '':
    home_name = 'HOME'

setOutput('home_name', home_name)

home_score = getOutput('home_score')
if home_score:
    if home_score.isnumeric():
        home_score = int(getOutput('home_score'))
    else:
        home_score = 0
else:
    home_score = 0

setOutput('home_score', home_score)

away_name = getOutput('away_name')
if away_name == '':
    away_name = 'AWAY'

setOutput('away_name', away_name)

away_score = getOutput('away_score')
if away_score:
    if away_score.isnumeric():
        away_score = int(getOutput('away_score'))
    else:
        away_score = 0

setOutput('away_score', away_score)

time = getOutput('time')
if not time:
    time = '00:00'
else:
    tmp = time.split(':')
    minutos = int(tmp[0])
    segundos = int(tmp[1])

setOutput('time', time)

# # TOOLBAR
toolbar = Frame(root, border=1, relief=RAISED)

btn_play = Button(toolbar, text=etiqueta, command=toggle)
btn_play.pack(side=LEFT, padx=2, pady=2)
setImage(btn_play, "assets/play.png")

btn_restart = Button(toolbar, text="Restart", command=restart)
btn_restart.pack(side=LEFT, padx=2, pady=2)
setImage(btn_restart, "assets/reload.png")

toolbar.place(x=0, y=0)
toolbar.pack(side=TOP, fill=X)

y = 75

lbl_home = Label(root, text="Home", width=22)
lbl_home.place(x=0, y=y)

txt_home_name = Entry(root, width=20,
                      font=('Arial', 18))
txt_home_name.place(x=50, y=y)
txt_home_name.bind("<FocusOut>", on_focus_out)
txt_home_name.insert(0, home_name)

btn_homescore_add = Button(root, text="+", width=10,
                           command=lambda: scoreUpdate('home_score', 1))
btn_homescore_add.place(x=320, y=y)
setImage(btn_homescore_add, "assets/caret-up.png")

txt_home_score = Entry(root, width=3,
                       font=('Arial', 18), justify=CENTER)
txt_home_score.place(x=355, y=y)
txt_home_score.bind("<FocusOut>", on_focus_out)
txt_home_score.insert(0, home_score)

btn_homescore_substract = Button(
    root, text="+", width=10, command=lambda: scoreUpdate('home_score', -1))
btn_homescore_substract.place(x=400, y=y)
setImage(btn_homescore_substract, "assets/arrow-down.png")

y = 110

lbl_away = Label(root, text="Away", width=22)
lbl_away.place(x=0, y=y)

txt_away_name = Entry(root, width=20,
                      font=('Arial', 18))
txt_away_name.place(x=50, y=y)
txt_away_name.bind("<FocusOut>", on_focus_out)
txt_away_name.insert(0, away_name)

btn_awayscore_add = Button(root, text="+", width=10,
                           command=lambda: scoreUpdate('away_score', 1))
btn_awayscore_add.place(x=320, y=y)
setImage(btn_awayscore_add, "assets/caret-up.png")

txt_away_score = Entry(root, width=3,
                       font=('Arial', 18), justify=CENTER)
txt_away_score.place(x=355, y=y)
txt_away_score.bind("<FocusOut>", on_focus_out)
txt_away_score.insert(0, away_score)

btn_awayscore_substract = Button(
    root, text="+", width=10, command=lambda: scoreUpdate('away_score', -1))
btn_awayscore_substract.place(x=400, y=y)
setImage(btn_awayscore_substract, "assets/arrow-down.png")


# TIME
y = 75

btn_time_minutes_add = Button(
    text="+", command=lambda: timeUpdate('minutos', 1))
btn_time_minutes_add.place(x=455, y=y)
setImage(btn_time_minutes_add, "assets/caret-up.png")

btn_time_minutes_substract = Button(
    text="+", command=lambda: timeUpdate('minutos', -1))
btn_time_minutes_substract.place(x=455, y=y+35)
setImage(btn_time_minutes_substract, "assets/arrow-down.png")

txt_time = Entry(root, width=5, font=('Arial', 40), justify=CENTER)
txt_time.insert(0, time)
txt_time.bind("<FocusOut>", on_focus_out)
txt_time.place(x=490, y=y)

lbl_time = Label(root, text=time, font=('Arial', 40), justify=CENTER)

x = 642

btn_time_seconds_add = Button(
    text="+", command=lambda: timeUpdate('segundos', 1))
btn_time_seconds_add.place(x=x, y=y)
setImage(btn_time_seconds_add, "assets/caret-up.png")

btn_time_seconds_substract = Button(
    text="+", command=lambda: timeUpdate('segundos', -1))
btn_time_seconds_substract.place(x=x, y=y+35)
setImage(btn_time_seconds_substract, "assets/arrow-down.png")

# spn_minutos.bind("<FocusOut>", on_focus_out)
# reloj_minutos = Entry(root, width=5)
# reloj_minutos.insert(0, "00")
# reloj_minutos.bind("<FocusOut>", on_focus_out)

# # SEGUNDOS
spn_segundos = Spinbox(from_=0, to=1000, increment=1,
                       command=lambda v='segundos': setTime(v))

root.mainloop()
