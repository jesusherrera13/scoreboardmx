from tkinter import *
from tkinter.ttk import *
import os
from time import strftime


def start():

    global home_score
    global away_score
    global segundos
    global minutos
    global play
    global etiqueta

    setOutput('HOME', 'home_name')
    setOutput('0', 'home_score')
    setOutput('away', 'away_name')
    setOutput('0', 'away_score')
    setOutput('00:00', 'time')

    play = False
    etiqueta = "Start"
    segundos = 0
    minutos = 0
    home_score = 0
    away_score = 0
    spn_minutos.set(minutos)
    spn_segundos.set(segundos)


def contador():

    global play
    global segundos
    global minutos
    global home_score
    global away_score

    if play:

        reloj_minutos.delete(0, END)
        reloj_segundos.delete(0, END)

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
        txt = m_ + ':' + s_

        reloj_minutos.insert(0, m_)
        reloj_segundos.insert(0, s_)

        spn_minutos.set(minutos)
        spn_segundos.set(segundos)

        setOutput(txt, 'time')
        # setOutput(m_, 'minutos')
        # setOutput(s_, 'segundos')

        lbl_time.config(text=txt)

        root.after(1000, contador)

        segundos += 1


def toggle():

    global etiqueta
    global play
    global visita

    play = not play
    if play:
        text = "Pause"
    else:
        text = "Start"

    btn_play.config(text=text)

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


def setOutput(texto, prefijo):
    global path
    try:
        if not os.path.isdir(path):
            os.mkdir(path)
    except OSError as error:
        print(error)

    with open(path + '/' + prefijo + '.txt', 'w') as f:
        f.write(texto.upper())


def callback(sv, prefijo):
    setOutput(sv.get(), prefijo)


def setTime(v):

    global minutos
    global segundos

    if v == 'minutos':
        minutos = int(spn_minutos.get())
    else:
        segundos = int(spn_segundos.get())


def on_focus_out(event):

    global minutos
    global segundos

    if play == False:
        if event.widget == reloj_minutos:
            if (reloj_minutos.get().isdecimal()):
                minutos = int(reloj_minutos.get())
        elif event.widget == reloj_segundos:
            if (reloj_segundos.get().isdecimal()):
                segundos = int(reloj_segundos.get())

    if event.widget == txt_home_name:
        setOutput(txt_home_name.get(), 'home_name')
    elif event.widget == txt_away_name:
        setOutput(txt_away_name.get(), 'away_name')

    if event.widget == spn_minutos:
        minutos = int(spn_minutos.get())
    elif event.widget == spn_segundos:
        segundos = int(spn_segundos.get())


def setScore(v):
    txt = ''
    if v == 'home_score':
        txt = spn_home_score.get()
    else:
        txt = spn_away_score.get()

    setOutput(txt, v)


def getOutput(name):
    f = open(name, 'r')
    print(f.read())


version = "v0.1"  # 2024-04-24
root = Tk()
root.geometry("600x200")
root.title("Scoreboard MX " + version + " - El Juego Perfecto MX")
root.resizable(False, False)

icon_file = "icon.ico"
if (os.path.exists(icon_file)):
    # img = PhotoImage(file='icon.png')
    # root.iconphoto(False, img)
    root.iconbitmap(icon_file)


global path
global etiqueta

path = "output"
etiqueta = "Start"
home_name = "Home"
home_score = 0
away_name = "Away"
away_score = 0

# HOME
lbl_home = Label(root, text="Home", anchor="w", justify=LEFT, width=22)
txt_home_name = Entry(root, width=30)
txt_home_name.bind("<FocusOut>", on_focus_out)
txt_home_name.insert(0, home_name)

# AWAY
lbl_away = Label(root, text="Away", anchor="w", justify=LEFT, width=22)
txt_away_name = Entry(root, width=30)
txt_away_name.bind("<FocusOut>", on_focus_out)
txt_away_name.insert(0, away_name)

# TIEMPO
lbl_tiempo = Label(root, text="Time", anchor="w", justify=LEFT, width=22)

spn_minutos = Spinbox(from_=0, to=1000, increment=1,
                      command=lambda v='minutos': setTime(v))
spn_minutos.bind("<FocusOut>", on_focus_out)
reloj_minutos = Entry(root, width=5)
reloj_minutos.insert(0, "00")
reloj_minutos.bind("<FocusOut>", on_focus_out)

# SEGUNDOS
spn_segundos = Spinbox(from_=0, to=1000, increment=1,
                       command=lambda v='segundos': setTime(v))
spn_segundos.bind("<FocusOut>", on_focus_out)
reloj_segundos = Entry(root, width=5)
reloj_segundos.bind("<FocusOut>", on_focus_out)
reloj_segundos.insert(0, "00")

spn_home_score = Spinbox(from_=0, to=1000, increment=1,
                         command=lambda v='home_score': setScore(v))
spn_home_score.set(home_score)

spn_away_score = Spinbox(from_=0, to=1000, increment=1,
                         command=lambda v='away_score': setScore(v))
spn_away_score.set(away_score)

lbl_time = Label(root, text="00:00", font=('Times New Roman', 24, 'bold'))

lbl_time.grid(row=2, column=0)
lbl_tiempo.grid(row=3, column=0)
spn_minutos.grid(row=3, column=1)
spn_segundos.grid(row=3, column=2)

lbl_team_name = Label(root, text="Name",
                      anchor="w", justify=LEFT, width=22)
lbl_team_name.grid(row=4, column=1)

lbl_team_score = Label(root, text="Score",
                       anchor="w", justify=LEFT, width=22)
lbl_team_score.grid(row=4, column=2)

lbl_home.grid(row=5, column=0)
txt_home_name.grid(row=5, column=1)
spn_home_score.grid(row=5, column=2)

lbl_away.grid(row=6, column=0)
txt_away_name.grid(row=6, column=1)
spn_away_score.grid(row=6, column=2)

btn_play = Button(root, text=etiqueta, command=toggle)
btn_restart = Button(root, text="Restart", command=restart)

btn_play.grid(row=1, column=0)
btn_restart.grid(row=1, column=1)

start()
root.mainloop()
