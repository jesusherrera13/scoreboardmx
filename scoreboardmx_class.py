import tkinter as tk
from tkinter import ttk, Menu, LEFT, TOP, X, RAISED, StringVar,Toplevel, Button, Frame, DISABLED, Label,Radiobutton, Entry, END, CENTER, WRITABLE, ACTIVE, filedialog as fd
import os
import platform
from PIL import Image, ImageTk
import shutil

class SecondaryWindow(Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=300, height=200)
        self.title("Secondary Window")
        self.resizable(False, False)
        self.button_close = Button(
            self,
            text="Close window",
            command=self.destroy
        )
        self.button_close.place(x=75, y=75)
        self.focus()
        self.grab_set()


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("850x300")
        self.resizable(False, False)
        self.version = "0.1"
        self.title("Scoreboard MX " + self.version)
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=False)
        filemenu.add_command(
            label="About",
            command=self.open_secondary_window,
            compound=LEFT
        )
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        self.path = "output"
        self.etiqueta = "Start"
        self.play = False
        self.clock_asc = True

        self.home_name = ""
        self.home_score = ""

        self.direction = StringVar()
        self.language = StringVar()

        self.diccionario = {
            "ES": {
                "team": "Equipo",
                "score": "Marcador",
                "timer": "Tiempo",
                "asc": "Ascendente",
                "desc": "Descendente",
                "label_play": "Iniciar"
            },
            "FR": {
                "team": "Équipe",
                "score": "Score",
                "timer": "Temps",
                "asc": "Ascendant",
                "desc": "Descendant",
                "label_play": "Commençer"
            },
            "EN": {
                "team": "Team",
                "score": "Score",
                "timer": "Time",
                "asc": "Ascendant",
                "desc": "Descending",
                "label_play": "start"
            },
            "ZH": {
                "team": "团队",
                "score": "总谱",
                "timer": "时间",
                "asc": "升序",
                "desc": "降序",
                "label_play": "开始"
            }
        }

        self.timer_direction = self.getOutput('timer_direction')
        if self.timer_direction:
            if self.timer_direction.upper() != 'ASC' and self.timer_direction.upper() != 'DESC':
                self.timer_direction = 'ASC'
        else:
            self.timer_direction = 'ASC'

        self.direction.set(self.timer_direction)

        if platform.system() == "Linux":
            im = Image.open('assets/icon.ico')
            photo = ImageTk.PhotoImage(im)
            self.wm_iconphoto(True, photo)
        elif platform.system() == "darwin":
            print("OS X")
        elif platform.system() == "Windows":
            img = "assets/icon.ico"
            if (os.path.exists(img)):
                self.iconbitmap(img)

        # SE ESTABLECE EL IDIOMA DE LA APP
        self.lang = self.getOutput('lang')
        if self.lang == '':
            self.lang = 'ES'

        # SE GUARDA EN ARCHIVO EL IDIOMA DE LA APP
        self.writeOutput('lang', self.lang)
        self.language.set(self.lang)

        # SE ESTABLECE LA CONFIGURACIÓN DE NOMBRE Y SCORE DEL HOME TEAM
        self.home_name = self.getOutput('home_name')
        if self.home_name == '':
            if self.lang == 'EN':
                self.home_name = 'HOME'
            else:
                self.home_name = 'CASA'

        self.writeOutput('home_name', self.home_name)

        self.home_score = self.getOutput('home_score')
        if self.home_score:
            if self.home_score.isnumeric():
                self.home_score = int(self.getOutput('home_score'))
            else:
                self.home_score = 0
        else:
            self.home_score = 0

        self.writeOutput('home_score', self.home_score)

        # SE ESTABLECE LA CONFIGURACIÓN DE NOMBRE Y SCORE DEL VISITANTE
        self.away_name = self.getOutput('away_name')
        if self.away_name == '':
            if self.lang == 'EN':
                self.away_name = 'AWAY'
            else:
                self.away_name = 'VISITA'

        self.writeOutput('away_name', self.away_name)

        self.away_score = self.getOutput('away_score')
        if self.away_score:
            if self.away_score.isnumeric():
                self.away_score = int(self.getOutput('away_score'))
            else:
                self.away_score = 0
        else:
            self.away_score = 0

        self.writeOutput('away_score', self.away_score)

        self.time = self.getOutput('time')
        if not self.time:
            self.time = '00:00'
            self.minutos = 0
            self.segundos = 0
        else:
            tmp = self.time.split(':')
            self.minutos = int(tmp[0])
            self.segundos = int(tmp[1])

        self.writeOutput('time', self.time)

        # TOOLBAR
        self.toolbar = Frame(self, border=1, relief=RAISED)

        self.btn_play = Button(self.toolbar, text=self.etiqueta, command=self.toggle)
        self.btn_play.pack(side=LEFT, padx=2, pady=2)

        self.btn_restart = Button(self.toolbar, text="Restart", command=self.restart)
        self.btn_restart.pack(side=LEFT, padx=2, pady=2)

        self.toolbar.place(x=0, y=0)
        self.toolbar.pack(side=TOP, fill=X)

        y = 50
        x = 5

        font = ('Arial', 12)
        self.lbl_team_1 = Label(self, text="Team", width=17, font=font, anchor="w", justify=LEFT)
        self.lbl_team_1.place(x=x, y=y)

        self.lbl_score_1 = Label(self, text="Score", width=22, font=font, anchor="w", justify=LEFT)
        self.lbl_score_1.place(x=x+197, y=y)

        self.lbl_timer = Label(self, text="Time", width=22, font=font)
        self.lbl_timer.place(x=x+295, y=y)

        options = [("Ascendant", "ASC"), ("Descendant", "DESC")]
        xx = 0

        for order, val in options:
            if val == "ASC":
                self.radio_asc = Radiobutton(self,
                                        text=order,
                                        # padx=20,
                                        variable=self.direction,
                                        command=self.toggleClock,
                                        value=val)
                self.radio_asc.place(x=x+295+xx, y=y+90)
            else:
                self.radio_desc = Radiobutton(self,
                                        text=order,
                                        # padx=20,
                                        variable=self.direction,
                                        command=self.toggleClock,
                                        value=val)
                self.radio_desc.place(x=x+295+xx, y=y+90)
            xx += 90

        btn_width = 25
        img_width = 100

        self.lbl_team_2 = Label(self, text="Score", width=btn_width, font=font, anchor="w", justify=LEFT)
        self.lbl_team_2.place(x=x+565, y=y)

        self.lbl_score_2 = Label(self, text="Team", width=btn_width, font=font, anchor="w", justify=LEFT)
        self.lbl_score_2.place(x=x+650, y=y)

        nw = 12
        y += 20
        x = 5

        self.txt_home_name = Entry(self, width=nw,
                            font=('Arial', 18))
        self.txt_home_name.place(x=x, y=y)
        self.txt_home_name.bind("<FocusOut>", self.on_focus_out)
        self.txt_home_name.insert(0, self.home_name)

        self.lbl_home = Label(self, text="Home logo", width=img_width,
                        borderwidth=1, relief="groove")
        self.lbl_home.bind("<Button-1>", lambda e: self.logo('home_logo'))
        self.lbl_home.place(x=x+25, y=y+50)

        self.btn_homescore_add = Button(self, text="+", width=btn_width,
                                command=lambda: self.scoreUpdate('home_score', 1))
        x = x + 165
        self.btn_homescore_add.place(x=x, y=y)

        self.txt_home_score = Entry(self, width=3,
                            font=('Arial', 18), justify=CENTER)
        x = x + 35

        self.txt_home_score.place(x=x, y=y)
        self.txt_home_score.bind("<FocusOut>", self.on_focus_out)
        self.txt_home_score.insert(0, self.home_score)

        x = x + 45

        self.btn_homescore_substract = Button(
            self, text="-", width=btn_width, command=lambda: self.scoreUpdate('home_score', -1))
        self.btn_homescore_substract.place(x=x, y=y)

        # TIME
        y = 70
        x = x + 50
        self.btn_time_minutes_add = Button(
            text="+", width=btn_width, command=lambda: self.timeUpdate('minutos', 1))
        self.btn_time_minutes_add.place(x=x, y=y)

        self.btn_time_minutes_substract = Button(
            text="-", width=btn_width, command=lambda: self.timeUpdate('minutos', -1))
        self.btn_time_minutes_substract.place(x=x, y=y+35)

        x = x + 35

        self.txt_time = Entry(self, width=5, font=('Arial', 40), justify=CENTER)
        self.txt_time.insert(0, self.time)
        self.txt_time.bind("<FocusOut>", self.on_focus_out)
        self.txt_time.place(x=x, y=y)
        # txt_time.config(bg="green")

        self.lbl_time = Label(self, text=self.time, font=('Arial', 40), justify=CENTER)

        x = x + 152

        self.btn_time_seconds_add = Button(
            text="+", width=btn_width, command=lambda: self.timeUpdate('segundos', 1))
        self.btn_time_seconds_add.place(x=x, y=y)

        self.btn_time_seconds_substract = Button(
            text="-",  width=btn_width, command=lambda: self.timeUpdate('segundos', -1))
        self.btn_time_seconds_substract.place(x=x, y=y+35)

        y = 70
        x += 50

        self.lbl_away = Label(self, text="Away logo", width=img_width,
                        borderwidth=1, relief="groove")
        self.lbl_away.bind("<Button-1>", lambda e: self.logo('away_logo'))
        self.lbl_away.place(x=x+145, y=y+50)

        self.btn_awayscore_add = Button(self, text="+", width=btn_width,
                                command=lambda: self.scoreUpdate('away_score', 1))
        self.btn_awayscore_add.place(x=x, y=y)

        x = x + 35

        self.txt_away_score = Entry(self, width=3,
                            font=('Arial', 18), justify=CENTER)
        self.txt_away_score.place(x=x, y=y)
        self.txt_away_score.bind("<FocusOut>", self.on_focus_out)
        self.txt_away_score.insert(0, self.away_score)

        x += 45
        self.btn_awayscore_substract = Button(
            self, text="-", width=btn_width, command=lambda: self.scoreUpdate('away_score', -1))
        self.btn_awayscore_substract.place(x=x, y=y)

        x += 40
        self.txt_away_name = Entry(self, width=nw,
                            font=('Arial', 18))
        self.txt_away_name.place(x=x, y=y)
        self.txt_away_name.bind("<FocusOut>", self.on_focus_out)
        self.txt_away_name.insert(0, self.away_name)

        options = [("Español", "ES"), ("Francés", "FR"),
                ("Inglés", "EN"), ("Chino", "ZH")]
        xx = 0
        count = 0
        for item, val in options:
            radio = Radiobutton(self.toolbar,
                                # text=item,
                                # padx=20,
                                variable=self.language,
                                command=self.setLanguage,
                                value=val)

            self.lbl = Label(self.toolbar, text=val, width=30,
                        borderwidth=1)
            self.setImage(self.lbl, "assets/"+val.lower()+".png")
            self.lbl.pack(side=LEFT)
            radio.pack(side=LEFT, padx=2)

            xx += 100

        self.setImage(self.btn_play, "assets/play.png")
        self.setImage(self.btn_homescore_add, "assets/caret-up.png")
        self.setImage(self.btn_homescore_substract, "assets/arrow-down.png")
        self.setImage(self.btn_restart, "assets/reload.png")
        self.setLogo(self.lbl_home)
        self.setLogo(self.lbl_away)
        self.setImage(self.btn_awayscore_substract, "assets/arrow-down.png")
        self.setImage(self.btn_time_minutes_add, "assets/caret-up.png")
        self.setImage(self.btn_time_minutes_substract, "assets/arrow-down.png")
        self.setImage(self.btn_time_seconds_add, "assets/caret-up.png")
        self.setImage(self.btn_time_seconds_substract, "assets/arrow-down.png")
        self.setImage(self.btn_awayscore_add, "assets/caret-up.png")
        self.setLanguage()

    def open_secondary_window(self):
        self.secondary_window = SecondaryWindow()

    def getOutput(self, target):
        file = 'output/' + target + '.txt'
        response = ''
        if (os.path.exists(file)):
            f = open(file, 'r')
            response = f.read()

        return response
    
    def contador(self):

        if self.play:
            inc = True
            if self.direction.get() == 'ASC':
                shift = 1
                if self.segundos > 59:
                    self.minutos += 1
                    self.segundos = 0
            else:
                shift = -1
                if self.segundos == 0 and self.minutos == 0:
                    self.txt_time.config({"foreground":"#ff0000"})
                    inc = False

                if inc and self.segundos == 0:
                    if (self.minutos > 0):
                        self.minutos -= 1
                    segundos = 59

            time_ = self.getTime()
            self.writeOutput('time', time_)
            self.lbl_time.config(text=time_)
            self.txt_time.delete(0, END)
            self.txt_time.insert(0, time_)
            self.after(1000, self.contador)
            
            if (inc):
                self.segundos += 1 * shift


    def writeOutput(self, target, value):
        try:
            if not os.path.isdir(self.path):
                os.mkdir(self.path)
        except OSError as error:
            print(error)

        with open(self.path + '/' + target + '.txt', 'w') as f:
            try:
                if target != 'home_logo' and target != 'away_logo':
                    value = str(value).upper()
                f.write(value)
            except OSError as error:
                print(error)


    def setLanguage(self):
        self.writeOutput('lang', self.language.get())
        self.lbl_team_1.config(text=self.diccionario[self.language.get()]["team"])
        self.lbl_team_2.config(text=self.diccionario[self.language.get()]["team"])
        self.lbl_score_1.config(text=self.diccionario[self.language.get()]["score"])
        self.lbl_score_2.config(text=self.diccionario[self.language.get()]["score"])
        self.lbl_timer.config(text=self.diccionario[self.language.get()]["timer"])
        self.radio_asc.config(text=self.diccionario[self.language.get()]["asc"])
        self.radio_desc.config(text=self.diccionario[self.language.get()]["desc"])

    def toggle(self):
        self.play = not self.play

        x = 335
        y = 71
        if self.play:
            img_path = "assets/pause.png"
            self.txt_time.place_forget()
            self.lbl_time.place(x=x+8, y=y)
            self.btn_time_minutes_add.config(state=DISABLED)
            self.btn_time_minutes_substract.config(state=DISABLED)
            self.btn_time_seconds_add.config(state=DISABLED)
            self.btn_time_seconds_substract.config(state=DISABLED)
        else:
            img_path = "assets/play.png"
            self.txt_time.place(x=x, y=y-1)
            self.lbl_time.place_forget()
            self.btn_time_minutes_add.config(state=ACTIVE)
            self.btn_time_minutes_substract.config(state=ACTIVE)
            self.btn_time_seconds_add.config(state=ACTIVE)
            self.btn_time_seconds_substract.config(state=ACTIVE)

        if (os.path.exists(img_path)):
            img = Image.open(img_path)
            eimg = ImageTk.PhotoImage(img)
            self.btn_play.config(image=eimg)
            self.btn_play.image_names = eimg

        self.contador()

    def toggleClock(self):
        self.writeOutput('timer_direction', self.direction.get())

    def on_focus_out(self, event):

        if self.play is False:
            if event.widget == self.txt_time:
                value = self.txt_time.get()
                if (value):
                    tmp = value.split(':')
                    if len(tmp) == 1:
                        if tmp[0].isnumeric():
                            self.minutos = 0
                            self.segundos = int(tmp[0])
                    elif len(tmp) == 2:
                        if not tmp[0].isnumeric():
                            tmp[0] = 0
                        if not tmp[1].isnumeric():
                            tmp[1] = 0

                        self.minutos = int(tmp[0])
                        self.segundos = int(tmp[1])

                    time_ = self.getTime()

                    self.writeOutput('time', time_)
                    self.txt_time.delete(0, END)
                    self.txt_time.insert(0, time_)
                    self.lbl_time.config(text=time_)
                else:
                    self.txt_time.delete(0, END)
                    self.txt_time.insert(0, self.getTime())

        if event.widget == self.txt_home_name:
            self.writeOutput('home_name',self. txt_home_name.get())
        elif event.widget == self.txt_away_name:
            self.writeOutput('away_name', self.txt_away_name.get())

        if event.widget == self.txt_home_score or event.widget == self.txt_away_score:
            widget = event.widget
            value = widget.get()

            if value.isnumeric():
                if widget == self.txt_home_score:
                    target = 'home_score'
                    self.home_score = int(value)
                elif widget == self.txt_away_score:
                    target = 'away_score'
                    self.away_score = int(value)

                self.writeOutput(target, value)
            else:
                if widget == self.txt_home_score:
                    value = self.home_score
                elif widget == self.txt_away_score:
                    value = self.away_score

                widget.delete(0, END)
                widget.insert(0, value)

    def getTime(self):
        # global segundos
        # global minutos

        s = str(self.segundos)
        s = s.zfill(2)
        m = str(self.minutos)
        m = m.zfill(2)

        return m + ':' + s
    
    def scoreUpdate(self, target, value):
        # global home_score
        # global away_score
        score = 0

        if target == 'home_score':
            self.home_score += value

            if self.home_score < 0:
                self.home_score = 0

            self.txt_home_score.delete(0, END)
            self.txt_home_score.insert(0, str(self.home_score))
            score = self.home_score

        if target == 'away_score':
            self.away_score += value

            if self.away_score < 0:
                self.away_score = 0

            self.txt_away_score.delete(0, END)
            self.txt_away_score.insert(0, str(self.away_score))
            score = self.away_score

        self.writeOutput(target, score)

    def setImage(self, widget, path):

        if (os.path.exists(path)):
            img = Image.open(path)

            if widget == self.lbl_home or widget == self.lbl_away:
                img.thumbnail((100, 100))  # Resize image if necessary

            eimg = ImageTk.PhotoImage(img)
            widget.config(image=eimg)
            widget.image_names = eimg

    def restart(self):
        self.segundos = 0
        self.minutos = 0
        self.home_score = 0
        self.away_score = 0
        time_ = self.getTime()
        self.txt_home_score.delete(0, END)
        self.txt_home_score.insert(0, self.home_score)
        self.txt_away_score.delete(0, END)
        self.txt_away_score.insert(0, self.away_score)
        self.txt_time.delete(0, END)
        self.txt_time.insert(0, time_)
        self.lbl_time.config(text=time_)
        self.writeOutput('time', time_)
        self.writeOutput('home_score', self.home_score)
        self.writeOutput('away_score', self.away_score)

    def setLogo(self, widget):

        if widget == self.lbl_home:
            file = 'home'
        elif widget == self.lbl_away:
            file = 'away'
        else:
            return
        logo = self.getOutput(file + '_logo')
        if logo:
            self.setImage(widget, 'output/' + logo)

    def timeUpdate(self, target, value):

        if not self.play:
            s = ''
            m = ''

            if target == 'segundos':
                self.segundos += value

                if self.segundos > 59:
                    self.minutos += 1
                    self.segundos = 0

                if self.segundos < 0:
                    if self.minutos >= 1:
                        self.segundos = 59
                        self.minutos -= 1
                    else:
                        self.segundos = 0

            if target == 'minutos':
                self.minutos += value

                if self.minutos < 0:
                    self.minutos = 0

            if (self.segundos < 10):
                s = '0'

            if (self.minutos < 10):
                m = '0'

            m_ = m + str(self.minutos)
            s_ = s + str(self.segundos)
            time_ = m_ + ':' + s_
            self.writeOutput('time', time_)
            self.lbl_time.config(text=time_)
            self.txt_time.delete(0, END)
            self.txt_time.insert(0, time_)

    def logo(self, target):
        filetypes = [('Image files', '.jpg .jpeg .png')]
        file_path = fd.askopenfilename(
            title='Open a file', initialdir='/', filetypes=filetypes)

        if file_path:
            image = Image.open(file_path)
            image.thumbnail((100, 100))  # Resize image if necessary
            photo = ImageTk.PhotoImage(image)

            if target == 'home_logo':
                self.lbl_home.config(image=photo)
                self.lbl_home.image = photo  # Keep a reference to avoid garbage collection
            elif target == 'away_logo':
                self.lbl_away.config(image=photo)
                self.lbl_away.image = photo  # Keep a reference to avoid garbage collection

            self.save_image(target, file_path)
    
    def save_image(self, target, file_path):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        filename = os.path.basename(file_path)
        tmp = os.path.splitext(filename)
        tmp_name = target + tmp[1]

        shutil.copy(file_path, os.path.join(self.path, tmp_name))
        self.writeOutput(target, tmp_name)

main_window = MainWindow()
main_window.mainloop()