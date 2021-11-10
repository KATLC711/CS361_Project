from tkinter import *
from tkinter import messagebox
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import webbrowser
import socket
import json
from PIL import Image as Pil_image, ImageTk as Pil_imageTk
import io
import pickle


def image_send_request(keywords, client):
    """
    Sends request with keywords to server.
    """
    client.send(keywords.encode())

def image_recv_response(client):
    """
    Receives image URLs as payload from server response.
    """
    response = client.recv(2048).decode()
    client.close()

    cnt = 0
    urls = []
    temp = ''
    check = False
    while cnt < len(response):
        if response[cnt] == "'" and temp == '':
            check = True
        elif response[cnt] == "'" and temp != '':
            check = False
            urls.append(temp)
            temp = ""
        elif check:
            temp = temp + response[cnt]

        cnt += 1

    return urls






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
    s.connect((socket.gethostname(), 1234))




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



    s = socket.socket()
    port = 12345
    s.connect((socket.gethostname(), port))

    image_send_request(keyword, s)
    urls = image_recv_response(s)

    image_list = []

    for link in urls:
        # print(link)
        image_list.append(
            Pil_imageTk.PhotoImage(Pil_image.open(io.BytesIO(urlopen(link).read())).resize((350, 300), Pil_image.ANTIALIAS)))


    my_label = Label(RightUp, image=image_list[0])
    my_label.grid(row=0, column=0, columnspan=3,padx = 75)

    #my_label = Label(RightUp, image = image_list[0])
    #my_label.grid(row=0, column=0,padx = 75, pady = 17)


    def forward(image_number):
        global my_label
        global button_forward
        global button_back

        #my_label.grid_forget()
        my_label = Label(RightUp,image=image_list[image_number - 1])
        button_forward = Button(RightUp, text=">>", command=lambda: forward(image_number + 1))
        button_back = Button(RightUp, text="<<", command=lambda: back(image_number - 1))

        if image_number == len(image_list):
            button_forward = Button(RightUp, text=">>", state=DISABLED)

        my_label.grid(row=0, column=0, columnspan=3)
        button_back.grid(row=1, column=0)
        button_exit.grid(row=1, column=1)
        button_forward.grid(row=1, column=2)


    def back(image_number):
        global my_label
        global button_forward
        global button_back

        #my_label.grid_forget()
        my_label = Label(RightUp,image=image_list[image_number - 1])
        button_forward = Button(RightUp, text=">>", command=lambda: forward(image_number + 1))
        button_back = Button(RightUp, text="<<", command=lambda: back(image_number - 1))

        if image_number == 1:
            button_back = Button(RightUp, text="<<", state=DISABLED)

        my_label.grid(row=0, column=0, columnspan=3)
        button_back.grid(row=1, column=0)
        button_exit.grid(row=1, column=1)
        button_forward.grid(row=1, column=2)

    button_back = Button(RightUp, text="<<", command=back, state=DISABLED)
    button_exit = Button(RightUp, text="Exit Program", command=gui.quit)
    button_forward = Button(RightUp, text=">>", command=lambda: forward(2))

    button_back.grid(row=1, column=0)
    button_exit.grid(row=1, column=1)
    button_forward.grid(row=1, column=2)





    FORMAT = 'utf-8'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5721))

    #function to receive reply from server
    def youtube_receive():
        msg = s.recv(1024)
        data = pickle.loads(msg)    #serialize using pickle
        return data

    #function to send request to server
    def youtube_send(msg):
        data = pickle.dumps(msg)
        s.send(data)

    youtube_send([keyword]) #input the name of the movie
    video_result = youtube_receive()


    Youtube_Link0 = Label(RightBtm, text="Youtube Title/Description", justify=LEFT)
    Youtube_Link0.grid(sticky = W,row=0, column=0, padx = 30, pady = 5)

    Youtube_Button0 = Label(RightBtm, text="Hyperlink", justify=LEFT)
    Youtube_Button0.grid(sticky = W,row=0, column=1, padx = 30, pady = 5)

    for i in range(len(video_result)):
        Youtube_Link = Label(RightBtm, text=video_result[i]["title"][0:50], justify=LEFT)
        Youtube_Link.grid(sticky=W, row=i+1, column=0, padx=30, pady=5)

        Youtube_Button = Button(RightBtm, text="Link", command = lambda i = i: callback(video_result[i]['url']))
        Youtube_Button.grid(row=i+1, column=1, padx=30, pady=5)



Top = Frame(gui, width=1000,height=80)
Left = Frame(gui, width=500, height=335)
RightUp = Frame(gui, width=500, height=335)
RightBtm = Frame(gui, width=500, height=335)

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







'''
my_img = Pil_image.open("Petey.JPG")

my_img_resized = my_img.resize((350, 300), Pil_image.ANTIALIAS)
my_img = Pil_imageTk.PhotoImage(my_img_resized)

my_label = Label(RightUp, image = my_img)
my_label.grid(row=0, column=0,padx = 75, pady = 17)


import io
url1 = "https://beccaboosandkimblebees.files.wordpress.com/"
url2 = "2013/02/tumblr_mhm8uaxf731rrufwao1_500_large.jpg"
pic_url = url1 + url2

# open the web page picture and read it into a memory stream
# and convert to an image Tkinter can handle
my_page = urlopen(pic_url)
# create an image file object
my_picture = io.BytesIO(my_page.read())
pil_img = Pil_image.open(my_picture)
# convert to an image Tkinter can use
tk_img = Pil_imageTk.PhotoImage(pil_img)

my_label = Label(RightUp, image = tk_img)
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
'''




gui.mainloop()

