from tkinter import *
from tkinter.ttk import *
import os
from tkinter.ttk import Style as Style_
from tkinter import LEFT, TOP, X, FLAT, RAISED
from PIL import Image, ImageTk
from tkinter import filedialog as fd, messagebox
import shutil


def contador():

    global play
    global segundos
    global minutos
    global home_score
    global away_score

    if play:
        inc = True
        if direction.get() == 'ASC':
            shift = 1
            if segundos > 59:
                minutos += 1
                segundos = 0
        else:
            shift = -1
            if segundos == 0 and minutos == 0:
                inc = False

            if inc and segundos == 0:
                if (minutos > 0):
                    minutos -= 1
                segundos = 59

        time_ = getTime()
        writeOutput('time', time_)
        lbl_time.config(text=time_)
        txt_time.delete(0, END)
        txt_time.insert(0, time_)
        root.after(1000, contador)

        if (inc):
            segundos += 1 * shift


def toggle():
    global etiqueta
    global play
    global visita
    play = not play

    x = 335
    y = 71
    if play:
        img_path = "assets/pause.png"
        txt_time.place_forget()
        lbl_time.place(x=x+8, y=y)
        btn_time_minutes_add.config(state=DISABLED)
        btn_time_minutes_substract.config(state=DISABLED)
        btn_time_seconds_add.config(state=DISABLED)
        btn_time_seconds_substract.config(state=DISABLED)
    else:
        img_path = "assets/play.png"
        txt_time.place(x=x, y=y-1)
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
    time_ = getTime()
    txt_home_score.delete(0, END)
    txt_home_score.insert(0, home_score)
    txt_away_score.delete(0, END)
    txt_away_score.insert(0, away_score)
    txt_time.delete(0, END)
    txt_time.insert(0, time_)
    lbl_time.config(text=time_)
    writeOutput('time', time_)
    writeOutput('home_score', home_score)
    writeOutput('away_score', away_score)


def writeOutput(target, value):
    global path

    try:
        if not os.path.isdir(path):
            os.mkdir(path)
    except OSError as error:
        print(error)

    with open(path + '/' + target + '.txt', 'w') as f:
        try:
            if target != 'home_logo' and target != 'away_logo':
                value = str(value).upper()
            f.write(value)
        except OSError as error:
            print(error)


def callback(sv, prefijo):
    writeOutput(sv.get(), prefijo)


def setTime(v):

    global minutos
    global segundos


def on_focus_out(event):
    global home_score
    global away_score
    global minutos
    global segundos

    if play == False:
        if event.widget == txt_time:
            value = txt_time.get()
            if (value):
                tmp = value.split(':')
                if len(tmp) == 1:
                    if tmp[0].isnumeric():
                        minutos = 0
                        segundos = int(tmp[0])
                elif len(tmp) == 2:
                    if not tmp[0].isnumeric():
                        tmp[0] = 0
                    if not tmp[1].isnumeric():
                        tmp[1] = 0

                    minutos = int(tmp[0])
                    segundos = int(tmp[1])

                time_ = getTime()

                writeOutput('time', time_)
                txt_time.delete(0, END)
                txt_time.insert(0, time_)
                lbl_time.config(text=time_)
            else:
                txt_time.delete(0, END)
                txt_time.insert(0, getTime())

    if event.widget == txt_home_name:
        writeOutput('home_name', txt_home_name.get())
    elif event.widget == txt_away_name:
        writeOutput('away_name', txt_away_name.get())

    if event.widget == txt_home_score or event.widget == txt_away_score:
        widget = event.widget
        value = widget.get()

        if value.isnumeric():
            if widget == txt_home_score:
                target = 'home_score'
                home_score = int(value)
            elif widget == txt_away_score:
                target = 'away_score'
                away_score = int(value)

            writeOutput(target, value)
        else:
            if widget == txt_home_score:
                value = home_score
            elif widget == txt_away_score:
                value = away_score

            widget.delete(0, END)
            widget.insert(0, value)


def setScore(v):
    txt = ''
    if v == 'home_score':
        txt = spn_home_score.get()
    else:
        txt = spn_away_score.get()

    writeOutput(txt, v)


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

    writeOutput(target, score)


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
        writeOutput('time', time_)
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

        if widget == lbl_home or widget == lbl_away:
            img.thumbnail((100, 100))  # Resize image if necessary

        eimg = ImageTk.PhotoImage(img)
        widget.config(image=eimg)
        widget.image_names = eimg


def logo(target):
    filetypes = [('Image files', '.jpg .jpeg .png')]
    file_path = fd.askopenfilename(
        title='Open a file', initialdir='/', filetypes=filetypes)

    if file_path:
        image = Image.open(file_path)
        image.thumbnail((100, 100))  # Resize image if necessary
        photo = ImageTk.PhotoImage(image)

        if target == 'home_logo':
            lbl_home.config(image=photo)
            lbl_home.image = photo  # Keep a reference to avoid garbage collection
        elif target == 'away_logo':
            lbl_away.config(image=photo)
            lbl_away.image = photo  # Keep a reference to avoid garbage collection

        save_image(target, file_path)


def save_image(target, file_path):
    global path
    if not os.path.exists(path):
        os.makedirs(path)

    filename = os.path.basename(file_path)
    tmp = os.path.splitext(filename)
    tmp_name = target + tmp[1]

    shutil.copy(file_path, os.path.join(path, tmp_name))
    writeOutput(target, tmp_name)


def setLogo(widget):

    if widget == lbl_home:
        file = 'home'
    elif widget == lbl_away:
        file = 'away'
    else:
        return
    logo = getOutput(file + '_logo')
    if logo:
        setImage(widget, 'output/' + logo)


def getTime():
    global segundos
    global minutos

    s = str(segundos)
    s = s.zfill(2)
    m = str(minutos)
    m = m.zfill(2)

    return m + ':' + s


def openNewWindow():
    newWindow = Toplevel(root)
    newWindow.title("ScoreboardMX")
    newWindow.geometry("300x200")
    newWindow.resizable(False, False)
    newWindow.attributes('-topmost', True)

    # A Label widget to show in toplevel
    text = "Scoreboard MX 1.0"
    text += "\n\n"
    text += "\neljuegoperfectomx13@gmail.com"
    text += "\n\n"
    text += "\nJesús Herrera"
    text += "\nLuis Franco"
    text += "\nYoby Mora"
    text += "\n\n"
    text += "\nMazatlán, Sinaloa, México"

    Label(newWindow,
          text=text).pack()


def toggleClock():
    global clock_asc
    writeOutput('timer_direction', direction.get())
############


version = "v0.1"  # 2024-04-24
root = Tk()
root.geometry("850x300")
root.title("Scoreboard MX")
root.resizable(False, False)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=False)
filemenu.add_command(
    label="About",
    command=openNewWindow,
    compound=LEFT
)

menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)

# VARS
global path
global etiqueta
global home_name
global home_score
global play
global clock_asc

play = False
path = "output"
etiqueta = "Start"
clock_asc = True

direction = StringVar()

timer_direction = getOutput('timer_direction')
if timer_direction:
    if timer_direction.upper() != 'ASC' and timer_direction.upper() != 'DESC':
        timer_direction = 'ASC'
else:
    timer_direction = 'ASC'

direction.set(timer_direction)
# VARS

img = "assets/icon.ico"
if (os.path.exists(img)):
    root.iconbitmap(img)

home_name = getOutput('home_name')
if home_name == '':
    home_name = 'HOME'

writeOutput('home_name', home_name)

home_score = getOutput('home_score')
if home_score:
    if home_score.isnumeric():
        home_score = int(getOutput('home_score'))
    else:
        home_score = 0
else:
    home_score = 0

writeOutput('home_score', home_score)

away_name = getOutput('away_name')
if away_name == '':
    away_name = 'AWAY'

writeOutput('away_name', away_name)

away_score = getOutput('away_score')
if away_score:
    if away_score.isnumeric():
        away_score = int(getOutput('away_score'))
    else:
        away_score = 0

writeOutput('away_score', away_score)

time = getOutput('time')
if not time:
    time = '00:00'
else:
    tmp = time.split(':')
    minutos = int(tmp[0])
    segundos = int(tmp[1])

writeOutput('time', time)

# # TOOLBAR
toolbar = Frame(root, border=1, relief=RAISED)

btn_play = Button(toolbar, text=etiqueta, command=toggle)
btn_play.pack(side=LEFT, padx=2, pady=2)

btn_restart = Button(toolbar, text="Restart", command=restart)
btn_restart.pack(side=LEFT, padx=2, pady=2)

toolbar.place(x=0, y=0)
toolbar.pack(side=TOP, fill=X)

y = 50
x = 5

font = ('Arial', 12)
lbl = Label(root, text="Team", width=22, font=font)
lbl.place(x=x, y=y)

lbl = Label(root, text="Score", width=22, font=font)
lbl.place(x=x+165, y=y)

lbl = Label(root, text="Time", width=22, font=font)
lbl.place(x=x+295, y=y)

options = [("Ascendant", "ASC"), ("Descendant", "DESC")]
xx = 0

for language, val in options:
    radio = Radiobutton(root,
                        text=language,
                        # padx=20,
                        variable=direction,
                        command=toggleClock,
                        value=val)
    radio.place(x=x+295+xx, y=y+90)
    xx += 80

lbl = Label(root, text="Score", width=22, font=font)
lbl.place(x=x+530, y=y)

lbl = Label(root, text="Team", width=22, font=font)
lbl.place(x=x+650, y=y)

nw = 12
y += 20
x = 5

txt_home_name = Entry(root, width=nw,
                      font=('Arial', 18))
txt_home_name.place(x=x, y=y)
txt_home_name.bind("<FocusOut>", on_focus_out)
txt_home_name.insert(0, home_name)

lbl_home = Label(root, text="Home logo", width=22,
                 borderwidth=1, relief="groove")
lbl_home.bind("<Button-1>", lambda e: logo('home_logo'))
lbl_home.place(x=x+25, y=y+50)

btn_homescore_add = Button(root, text="+", width=10,
                           command=lambda: scoreUpdate('home_score', 1))
x = x + 165
btn_homescore_add.place(x=x, y=y)

txt_home_score = Entry(root, width=3,
                       font=('Arial', 18), justify=CENTER)
x = x + 35

txt_home_score.place(x=x, y=y)
txt_home_score.bind("<FocusOut>", on_focus_out)
txt_home_score.insert(0, home_score)

x = x + 45

btn_homescore_substract = Button(
    root, text="+", width=10, command=lambda: scoreUpdate('home_score', -1))
btn_homescore_substract.place(x=x, y=y)

# TIME
y = 70
x = x + 50
btn_time_minutes_add = Button(
    text="+", command=lambda: timeUpdate('minutos', 1))
btn_time_minutes_add.place(x=x, y=y)

btn_time_minutes_substract = Button(
    text="+", command=lambda: timeUpdate('minutos', -1))
btn_time_minutes_substract.place(x=x, y=y+35)

x = x + 35

txt_time = Entry(root, width=5, font=('Arial', 40), justify=CENTER)
txt_time.insert(0, time)
txt_time.bind("<FocusOut>", on_focus_out)
txt_time.place(x=x, y=y)

lbl_time = Label(root, text=time, font=('Arial', 40), justify=CENTER)

x = x + 152

btn_time_seconds_add = Button(
    text="+", command=lambda: timeUpdate('segundos', 1))
btn_time_seconds_add.place(x=x, y=y)

btn_time_seconds_substract = Button(
    text="+", command=lambda: timeUpdate('segundos', -1))
btn_time_seconds_substract.place(x=x, y=y+35)

y = 70
x += 50

lbl_away = Label(root, text="Away logo", width=22,
                 borderwidth=1, relief="groove")
lbl_away.bind("<Button-1>", lambda e: logo('away_logo'))
lbl_away.place(x=x+145, y=y+50)

btn_awayscore_add = Button(root, text="+", width=10,
                           command=lambda: scoreUpdate('away_score', 1))
btn_awayscore_add.place(x=x, y=y)

x = x + 35

txt_away_score = Entry(root, width=3,
                       font=('Arial', 18), justify=CENTER)
txt_away_score.place(x=x, y=y)
txt_away_score.bind("<FocusOut>", on_focus_out)
txt_away_score.insert(0, away_score)

x += 45
btn_awayscore_substract = Button(
    root, text="+", width=10, command=lambda: scoreUpdate('away_score', -1))
btn_awayscore_substract.place(x=x, y=y)

x += 40
txt_away_name = Entry(root, width=nw,
                      font=('Arial', 18))
txt_away_name.place(x=x, y=y)
txt_away_name.bind("<FocusOut>", on_focus_out)
txt_away_name.insert(0, away_name)

setImage(btn_play, "assets/play.png")
setImage(btn_homescore_add, "assets/caret-up.png")
setImage(btn_homescore_substract, "assets/arrow-down.png")
setImage(btn_restart, "assets/reload.png")
setLogo(lbl_home)
setLogo(lbl_away)
setImage(btn_awayscore_substract, "assets/arrow-down.png")
setImage(btn_time_minutes_add, "assets/caret-up.png")
setImage(btn_time_minutes_substract, "assets/arrow-down.png")
setImage(btn_time_seconds_add, "assets/caret-up.png")
setImage(btn_time_seconds_substract, "assets/arrow-down.png")
setImage(btn_awayscore_add, "assets/caret-up.png")

root.mainloop()
