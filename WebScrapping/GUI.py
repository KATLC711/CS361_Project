from tkinter import *
from tkinter import messagebox
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import webbrowser
import socket
import json
from PIL import Image as Pil_image, ImageTk as Pil_imageTk


gui = Tk()
gui.title("CS361 - Keyword Web Scrapping")
gui.geometry("1000x750")


def do_layout():
    Top.grid(row=0, column=0, columnspan = 2, sticky="nsew")
    Left.grid(row=1, column=0, rowspan = 2, sticky="nsew")
    RightUp.grid(row=1, column=1, sticky="nsew")
    RightBtm.grid(row=2, column=1, sticky="nsew")

    Top.grid_propagate(0)
    Left.grid_propagate(0)
    RightUp.grid_propagate(0)
    RightBtm.grid_propagate(0)

    gui.grid_rowconfigure(0, weight=1)
    gui.grid_columnconfigure(1, weight=1)


def callback(url):
    webbrowser.open_new(url)


def placeholder(msg):
    messagebox.showinfo("Webscraping", msg)



def web_scrapping():
    #messagebox.showinfo("Webscraping", keyword_entry.get())

    keyword = keyword_entry.get()

    HEADERSIZE = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((socket.gethostname(), 1234))
    s.connect((socket.gethostname(), 7699))




    s.send(keyword.encode("utf-8"))


    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            #print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msglen:
            #print("full msg received")

            d = json.loads(full_msg[HEADERSIZE:])
            #print(d)

            new_msg = True
            full_msg = ''
            break

    title = Label(Left, text="Title", justify=CENTER)
    title.grid(sticky = W,row=0, column=0)

    Search_PF = Label(Left, text="Search Platform", justify=CENTER)
    Search_PF.grid(sticky = W,row=0, column=1)

    Link = Label(Left, text="Link", justify=CENTER)
    Link.grid(sticky = W,row=0, column=2)



    for i in range(len(d['title'])):
        title = Label(Left, text=d['title'][i][0:50] + "...", justify=LEFT)
        title.grid(sticky = W,row=i+1, column=0)

        Search_PF = Label(Left, text=d['search_pf'][i], justify=LEFT)
        Search_PF.grid(sticky = W,row=i+1, column=1)

        link = Button(Left, text="Link", command = lambda i = i: callback(d['link'][i]))
        link.grid(row=i+1, column=2, padx = 5)



Top = Frame(gui, width=1000,height=80)
Left = Frame(gui, width=500, height=335)
RightUp = Frame(gui, bg='red', width=500, height=335)
RightBtm = Frame(gui, bg='green', width=500, height=335)

do_layout()


Top_Frame = LabelFrame(Top, text = "Current Setting", padx = 5, pady = 5)
Top_Frame.pack(expand = 1,fill = "both", padx = 10, pady = 10)

keyword_prompt = Label(Top_Frame, text="Please enter your keyword: ")
keyword_prompt.grid(row = 0, column = 0)
keyword_entry = Entry(Top_Frame, width = 35)
keyword_entry.grid(row = 0, column = 1)
Start_Search = Button(Top_Frame, text = "Start", command = web_scrapping)
Start_Search.grid(row = 0, column = 2, padx = 5)


my_menu = Menu(gui)
gui.config(menu = my_menu)

option_menu = Menu(my_menu)
my_menu.add_cascade(label="Option", menu=option_menu)
option_menu.add_command(label="Keywords", command= lambda: placeholder("This is the placeholder for keyword settings."))
option_menu.add_separator()
option_menu.add_command(label="Frequency", command= lambda: placeholder("This is the placeholder for frequency settings."))
option_menu.add_separator()
option_menu.add_command(label="Result Communication", command= lambda: placeholder("This is the placeholder for Result communication settings."))


history_menu = Menu(my_menu)
my_menu.add_cascade(label="History", menu=history_menu)
history_menu.add_command(label="History", command= lambda: placeholder("This is the placeholder for searching history."))




about_menu = Menu(my_menu)
my_menu.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="Guidelines", command= lambda: placeholder("This is the placeholder for Guidelines settings."))
about_menu.add_separator()
about_menu.add_command(label="About", command= lambda: placeholder("This is the placeholder for About."))




my_img = Pil_image.open("Petey.JPG")

my_img_resized = my_img.resize((350, 300), Pil_image.ANTIALIAS)
my_img = Pil_imageTk.PhotoImage(my_img_resized)

my_label = Label(RightUp, image = my_img)
my_label.grid(row=0, column=0,padx = 75, pady = 17)



Youtube_Link0 = Label(RightBtm, text="Youtube Title/Description", justify=LEFT)
Youtube_Link0.grid(sticky = W,row=0, column=0, padx = 30, pady = 5)

Youtube_Button0 = Label(RightBtm, text="Hyperlink", justify=LEFT)
Youtube_Button0.grid(sticky = W,row=0, column=1, padx = 30, pady = 5)


Youtube_Link1 = Label(RightBtm, text="Youtube Description 1", justify=LEFT)
Youtube_Link1.grid(sticky = W,row=1, column=0, padx = 30, pady = 5)

Youtube_Button1 = Button(RightBtm, text="Link")
Youtube_Button1.grid(row=1, column=1, padx=30, pady = 5)


Youtube_Link2 = Label(RightBtm, text="Youtube Description 2", justify=LEFT)
Youtube_Link2.grid(sticky = W,row=2, column=0, padx = 30, pady = 5)

Youtube_Button2 = Button(RightBtm, text="Link")
Youtube_Button2.grid(row=2, column=1, padx=30, pady = 5)


Youtube_Link3 = Label(RightBtm, text="Youtube Description 3", justify=LEFT)
Youtube_Link3.grid(sticky = W,row=3, column=0, padx = 30, pady = 5)

Youtube_Button3 = Button(RightBtm, text="Link")
Youtube_Button3.grid(row=3, column=1, padx=30, pady = 5)


Youtube_Link4 = Label(RightBtm, text="Youtube Description 4", justify=LEFT)
Youtube_Link4.grid(sticky = W,row=4, column=0, padx = 30, pady = 5)

Youtube_Button4 = Button(RightBtm, text="Link")
Youtube_Button4.grid(row=4, column=1, padx=30, pady = 5)




gui.mainloop()

