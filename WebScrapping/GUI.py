from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import webbrowser
import socket
import json
from PIL import Image as Pil_image, ImageTk as Pil_imageTk
import io
import pickle
import time, threading
import tkinter.messagebox as tkMessageBox
import smtplib
from datetime import datetime
from twilio.rest import Client
global email_checked, text_checked, email_entry_status, text_entry_status, result_communication, email_entry, text_entry
global freq_run, freq_stop, keyword_entry, search_history, history
global keyword_combination, option1_status, option2_status, option3_status, keyword1_status, keyword2_status, keyword3_status, keyword4_status
global keyword1, keyword2, keyword3, keyword4, option1, option2, option3


image_header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}

email_address = 'haycthtw@gmail.com'
email_password = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


freq_option = ["1 mins", "5 mins", "10 mins", "30 mins", "60 mins", "6 hrs", "24 hrs"]
freq_dict = {"1 mins" : 60000, "5 mins" : 300000, "10 mins":600000, "30 mins":1800000, "60 mins":3600000, "6 hrs":10800000, "24 hrs":64800000}

search_history = []



def frequency_popup():
    '''Function to pop up the frequency top level'''
    global freq_run
    freq_run = True
    freq = Toplevel()
    freq.geometry("500x350")
    freq.wm_title("Frequency Setting")

    freq_keyword_prompt2 = Label(freq,text="Select an appropriate time interval. If the frequency is high, it may overload your GUI. ")
    freq_keyword_prompt2.pack(pady=10)

    freq_keyword_prompt = Label(freq, text="Please select your keyword: ").pack(pady=10)
    freq_keyword_entry = Entry(freq)
    freq_keyword_entry.pack()

    prompt = Label(freq, text="Please select your time interval: ").pack(pady=10)
    my_combo = ttk.Combobox(freq, value=freq_option)
    my_combo.current(0)
    my_combo.pack(pady=20)

    def freq_execute():
        '''function to execute the frequency webscrapping '''
        global freq_stop

        keyword = freq_keyword_entry.get()
        time_interval = freq_dict[my_combo.get()]

        freq_stop = Button(Top_Frame, text="Stop", command=lambda: stop(freq_stop))
        freq_stop.grid(row = 0, column = 3, columnspan = 3, padx = 5)

        freq.destroy()

        def freq_execute_helper():
            if freq_run:
                print(time_interval)
                web_scrapping(keyword)
                Left.after(time_interval, freq_execute_helper)

        freq_execute_helper()




    freq_button = Button(freq, text="Enter", command = freq_execute)
    freq_button.pack()


    freq.mainloop()

def stop(obj):
    """Stop scanning by setting the global flag to False."""
    global freq_run
    global freq_stop
    freq_stop.destroy()
    freq_run = False


email_status = 0
text_status = 0
email_entry_status = ''
text_entry_status = ''



def result_popup():
    '''Function to pop up the result communication toplevel'''
    global email_checked, text_checked, email_entry_status, text_entry_status, result_communication, email_entry, text_entry, text_status, email_status
    result_launch()
    result_communication.deiconify()



def result_hide():
    '''Function to hide the result communication toplevel'''
    global email_checked, text_checked, email_entry_status, text_entry_status, result_communication, email_entry, text_entry, text_status, email_status
    email_entry_status = email_entry.get()
    text_entry_status = text_entry.get()
    email_status = email_checked.get()
    text_status = text_checked.get()
    print(email_status, text_status)
    result_communication.destroy()


def result_launch():
    '''Initaiilize the result communication toplevel'''
    global email_checked, text_checked, email_entry_status, text_entry_status, result_communication, email_entry, text_entry, text_status, email_status

    result_communication = Toplevel()
    result_communication.geometry("500x350")
    result_communication.wm_title("Result Communication Setting")
    email_checked =  IntVar()
    text_checked =  IntVar()
    email_checked.set(email_status)
    text_checked.set(text_status)

    result_prompt = Label(result_communication, text="Please select your desired way to communicate the result.").pack(pady=10)
    sep = ttk.Separator(result_communication,orient='horizontal')
    sep.pack(fill = 'x')

    email = Checkbutton(result_communication, text="Email", variable = email_checked, onvalue = 1, offvalue = 0)
    email.pack()
    email_prompt = Label(result_communication, text="Please enter your email: ").pack()
    email_entry = Entry(result_communication)
    email_entry.pack(pady = 10)
    sep = ttk.Separator(result_communication,orient='horizontal')
    sep.pack(fill = 'x')

    text = Checkbutton(result_communication, text="Text", variable = text_checked, onvalue = 1, offvalue = 0)
    text.pack()
    text_prompt = Label(result_communication, text="Please enter your phone number: ").pack()
    text_entry = Entry(result_communication)
    text_entry.pack(pady = 10)
    sep = ttk.Separator(result_communication,orient='horizontal')
    sep.pack(fill = 'x')

    text_entry.insert("end", text_entry_status)
    email_entry.insert("end", email_entry_status)


    Hide = Button(result_communication, text = "Enter", command = result_hide)
    Hide.pack(pady = 10)

    result_communication.withdraw()






def history_popup():
    '''function to show the history toplevel'''
    global history, search_history
    history_launch()
    history.deiconify()



def history_hide():
    '''function to hide the history toplevel'''
    global history, search_history
    history.withdraw()


def history_reset(keyword_string):
    '''function to re-use the keyword'''
    global keyword_entry, history

    keyword_entry.delete(0, END)
    keyword_entry.insert(0, keyword_string)
    history.withdraw()



def history_launch():
    '''function to initialize the history toplevel'''
    global search_history, history

    history = Toplevel()
    history.geometry("500x350")
    history.wm_title("Search History")

    history.grid_columnconfigure(1, weight=1)

    history_title = Label(history, text = "Keyword", justify=CENTER)
    history_title.grid(row = 0, column = 0, sticky = "WE", padx = 10, pady = 10)

    history_time = Label(history, text = "Search Time", justify=CENTER)
    history_time.grid(row = 0, column = 1, sticky = "WE", padx = 10, pady = 10)


    history.grid_columnconfigure(1, weight=1)

    history_title = Label(history, text = "Keyword", justify=CENTER)
    history_title.grid(row = 0, column = 0, sticky = "WE", padx = 10, pady = 10)

    history_time = Label(history, text = "Search Time", justify=CENTER)
    history_time.grid(row = 0, column = 1, sticky = "WE", padx = 10, pady = 10)

    history_button = Label(history, text = "Reuse Keyword", justify=CENTER)
    history_button.grid(row = 0, column = 2, sticky = "WE", padx = 10, pady = 10)

    cnt = 1

    for i in range(min(len(search_history),10), max(min(len(search_history),10) - 10, 0), -1):


        history_title = Label(history, text=search_history[i-1][0], justify=CENTER)
        history_title.grid(row=cnt+1, column=0, sticky="WE")

        history_time = Label(history, text=search_history[i-1][1], justify=CENTER)
        history_time.grid(row=cnt+1, column=1, sticky="WE")

        temp = search_history[i-1][0]
        history_button = Button(history, text="Reuse", command = lambda temp = temp :history_reset(temp))
        history_button.grid(row=cnt+1, column=2, padx = 20)

        cnt += 1

    history.withdraw()






def send_email(msg, recipent):
    '''function to send out webscrapping result via email'''
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email_address, email_password)

        smtp.sendmail(email_address,recipent, msg.encode('utf-8'))


def send_text(msg, recipent):
    '''function to send out web scrapping result via text'''
    account_sid = 'AC86b8bf8ca08fd5478f9ac4fd9ac7dcd9'
    auth_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=msg,
        from_='+17406933900',
        to=recipent
    )



option1_status = 'N/A'
option2_status = 'N/A'
option3_status = 'N/A'
keyword1_status = ''
keyword2_status = ''
keyword3_status = ''
keyword4_status = ''



def keyword_popup():
    '''Function to pop up the keyword toplevel'''
    global keyword_combination, option1_status, option2_status, option3_status, keyword1_status, keyword2_status, keyword3_status, keyword4_status, keyword1, keyword2, keyword3, keyword4, option1, option2, option3
    keyword_launch()
    keyword_combination.deiconify()



def keywrod_hide():
    '''Function to hide the keyword toplevel'''
    global keyword_combination, option1_status, option2_status, option3_status, keyword1_status, keyword2_status, keyword3_status, keyword4_status, keyword1, keyword2, keyword3, keyword4, option1, option2, option3
    option1_status = option1.get()
    option2_status = option2.get()
    option3_status = option3.get()
    keyword1_status = keyword1.get()
    keyword2_status = keyword2.get()
    keyword3_status = keyword3.get()
    keyword4_status = keyword4.get()
    keyword_combination.withdraw()




def keyword_launch():
    '''Function to initialize the keyword toplevel'''
    global keyword_combination, option1_status, option2_status, option3_status, keyword1_status, keyword2_status, keyword3_status, keyword4_status, keyword1, keyword2, keyword3, keyword4, option1, option2, option3

    keyword_options = ["N/A","AND","OR"]

    option1 = StringVar()
    option1.set(option1_status)
    option2 = StringVar()
    option2.set(option2_status)
    option3 = StringVar()
    option3.set(option3_status)


    keyword_combination = Toplevel()
    keyword_combination.geometry("500x350")
    keyword_combination.wm_title("Keyword Setting")

    def keyword_enter():
        '''Transfer the combined keyword to entry box in main GUI'''
        global keyword_entry
        global keyword_combination, option1_status, option2_status, option3_status, keyword1_status, keyword2_status, keyword3_status, keyword4_status, keyword1, keyword2, keyword3, keyword4, option1, option2, option3
        option1_status = option1.get()
        option2_status = option2.get()
        option3_status = option3.get()
        keyword1_status = keyword1.get()
        keyword2_status = keyword2.get()
        keyword3_status = keyword3.get()
        keyword4_status = keyword4.get()
        keyword_combination.withdraw()

        keyword_string = '"' + keyword1.get() + '"'


        if option1.get() == "AND":
            keyword_string += '+"' + keyword2.get() + '"'
        elif option1.get() == "OR":
            keyword_string += ' OR "' + keyword2.get() + '"'

        if option2.get() == "AND":
            keyword_string += '+"' + keyword3.get() + '"'
        elif option2.get() == "OR":
            keyword_string += ' OR "' + keyword3.get() + '"'

        if option3.get() == "AND":
            keyword_string += '+"' + keyword4.get() + '"'
        elif option3.get() == "OR":
            keyword_string += ' OR "' + keyword4.get() + '"'

        keyword_entry.delete(0, END)
        keyword_entry.insert(0,keyword_string)




    keyword_prompt = Label(keyword_combination, text = "Please enter your keyword below")
    keyword_prompt.pack(pady = 10)

    keyword1 = Entry(keyword_combination)
    keyword1.pack(pady = 5)

    keyword1_option = OptionMenu(keyword_combination, option1, *keyword_options)
    keyword1_option.pack(pady = 5)

    keyword2 = Entry(keyword_combination)
    keyword2.pack(pady = 5)

    keyword2_option = OptionMenu(keyword_combination, option2, *keyword_options)
    keyword2_option.pack(pady = 5)


    keyword3 = Entry(keyword_combination)
    keyword3.pack(pady = 5)

    keyword3_option = OptionMenu(keyword_combination, option3, *keyword_options)
    keyword3_option.pack(pady = 5)

    keyword4 = Entry(keyword_combination)
    keyword4.pack(pady = 5)

    keyword_enter_prompt = Button(keyword_combination, text="Enter", command=keyword_enter)
    keyword_enter_prompt.pack()

    keyword1.insert("end", keyword1_status)
    keyword2.insert("end", keyword2_status)
    keyword3.insert("end", keyword3_status)
    keyword4.insert("end", keyword4_status)


    keyword_combination.withdraw()



def instruction_popup():
    '''Function to pop up the instruction toplevel'''
    global instruction_page
    instruction_page.deiconify()



def instruction_hide():
    '''Function to hide the instruction toplevel'''
    global instruction_page
    instruction_page.withdraw()




def instruction_launch():
    '''Function to initialize the instruction toplevel'''
    global instruction_page


    instruction_page = Toplevel()
    instruction_page.geometry("500x350")
    instruction_page.wm_title("Instruction")


    Keyword_header = Label(instruction_page, text = "Start Search", font = "bold", justify=LEFT)
    Keyword_header.pack(padx = 10, pady = 1, anchor = "w")

    Keyword_instruction = Label(instruction_page, text = "Input your keyword at the front page and press enter to start the search. You will receive the text/image/Youtube Webscrapping result in a while. Note that the image scrapping services may take a little while.", wraplength=450, justify=LEFT)
    Keyword_instruction.pack(padx = 10, anchor = "w")


    Keyword_header = Label(instruction_page, text = "Timer", font = "bold", justify=LEFT)
    Keyword_header.pack(padx = 10, pady = 1, anchor = "w")

    Keyword_instruction = Label(instruction_page, text = "Input your keyword and select the frequency in the Frequency window under Option Menu. Click Enter and the webscrapping result will be delivered at the selected time interval. Click Stop at the GUI to stop the function. Compatible with the Result Communication options.", wraplength=450, justify=LEFT)
    Keyword_instruction.pack(padx = 10, anchor = "w")


    Keyword_header = Label(instruction_page, text = "Result Communication", font = "bold", justify=LEFT)
    Keyword_header.pack(padx = 10, pady = 1, anchor = "w")

    Keyword_instruction = Label(instruction_page, text = "Open the Result Communication under Option Menu. Select your desired method to communicate the result and input your personal email/phone number. ", wraplength=450, justify=LEFT)
    Keyword_instruction.pack(padx = 10, anchor = "w")

    Keyword_header = Label(instruction_page, text = "History", font = "bold", justify=LEFT)
    Keyword_header.pack(padx = 10, pady = 1, anchor = "w")

    Keyword_instruction = Label(instruction_page, text = "Open the History under History Menu. Your historical search record will be displayed here and there will be options allowing the reuse of these keywords.", wraplength=450, justify=LEFT)
    Keyword_instruction.pack(padx = 10, anchor = "w")

    Keyword_Exit = Button(instruction_page, text="Exit", command=instruction_hide)
    Keyword_Exit.pack(padx = 10, pady = 10)

    instruction_page.withdraw()






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
    '''Create layout for the main GUI'''
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
    '''Send out warning msg'''
    messagebox.showinfo("Webscraping", msg)


def text_scrapping(keyword):
    '''Performing text scrapping'''
    global email_checked, text_checked, search_history
    HEADERSIZE = 10

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1234))

    s.send(keyword.encode("utf-8"))


    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msglen:
            d = json.loads(full_msg[HEADERSIZE:])

            new_msg = True
            full_msg = ''
            break

    title = Label(Left, text="Title", justify=CENTER)
    title.grid(sticky = W,row=0, column=0)

    Search_PF = Label(Left, text="Search Platform", justify=CENTER)
    Search_PF.grid(sticky = W,row=0, column=1)

    Link = Label(Left, text="Link", justify=CENTER)
    Link.grid(sticky = W,row=0, column=2)



    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d-%H:%M:%S')
    subject = "Your WebScrapping Result at " + current_time
    body = ''
    msg_body = ''

    search_history.append([keyword, current_time])

    for i in range(len(d['title'])):
        title = Label(Left, text=d['title'][i][0:50] + "...", justify=LEFT)
        title.grid(sticky = W,row=i+1, column=0)

        Search_PF = Label(Left, text=d['search_pf'][i], justify=LEFT)
        Search_PF.grid(sticky = W,row=i+1, column=1)

        link = Button(Left, text="Link", command = lambda i = i: callback(d['link'][i]))
        link.grid(row=i+1, column=2, padx = 5)

        body = body + str(i + 1) + '. Title: ' + d['title'][i][0:50] + '\n' + 'Search Platform: ' + d['search_pf'][i] + '\n' + 'Link: ' + d['link'][i] + '\n\n\n'
        if i < 5:
            msg_body = msg_body + str(i + 1) + '. Title: ' + d['title'][i][0:50] + '\n' + 'Search Platform: ' + d['search_pf'][i] + '\n' + 'Link: ' + d['link'][i] + '\n'

    msg = f'Subject: {subject}\n\n{body}'
    msg_body = f'Subject: {subject}\n\n{msg_body}'


    if email_status == 1:
        send_email(msg, email_entry_status)

    if text_status == 1:
        send_text(msg_body, text_entry_status)




def image_scrapping(keyword):
    '''image scrapping services'''
    global email_checked, text_checked, search_history
    s = socket.socket()
    port = 12345
    s.connect((socket.gethostname(), port))

    image_send_request(keyword, s)
    urls = image_recv_response(s)

    image_list = []

    for link in urls:
        try:
            image_list.append(
                Pil_imageTk.PhotoImage(Pil_image.open(io.BytesIO(urlopen(link).read())).resize((350, 300), Pil_image.ANTIALIAS)))
        except Exception:
            pass


    my_label = Label(RightUp, image=image_list[0])
    my_label.grid(row=0, column=0, columnspan=3,padx = 75)


    def forward(image_number):
        global my_label
        global button_forward
        global button_back


        my_label = Label(RightUp,image=image_list[image_number - 1])
        button_forward = Button(RightUp, text=">>", command=lambda: forward(image_number + 1))
        button_back = Button(RightUp, text="<<", command=lambda: back(image_number - 1))

        if image_number == len(image_list):
            button_forward = Button(RightUp, text=">>", state=DISABLED)

        my_label.grid(row=0, column=0, columnspan=3)
        button_back.grid(row=1, column=0)

        button_forward.grid(row=1, column=2)


    def back(image_number):
        global my_label
        global button_forward
        global button_back


        my_label = Label(RightUp,image=image_list[image_number - 1])
        button_forward = Button(RightUp, text=">>", command=lambda: forward(image_number + 1))
        button_back = Button(RightUp, text="<<", command=lambda: back(image_number - 1))

        if image_number == 1:
            button_back = Button(RightUp, text="<<", state=DISABLED)

        my_label.grid(row=0, column=0, columnspan=3)
        button_back.grid(row=1, column=0)

        button_forward.grid(row=1, column=2)

    button_back = Button(RightUp, text="<<", command=back, state=DISABLED)

    button_forward = Button(RightUp, text=">>", command=lambda: forward(2))

    button_back.grid(row=1, column=0)

    button_forward.grid(row=1, column=2)



def youtube_scrapping(keyword):
    '''youtube scrapping'''
    global email_checked, text_checked, search_history
    FORMAT = 'utf-8'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5721))


    def youtube_receive():
        msg = s.recv(1024)
        data = pickle.loads(msg)
        return data


    def youtube_send(msg):
        data = pickle.dumps(msg)
        s.send(data)

    youtube_send([keyword])
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




def web_scrapping(keyword):
    '''Main function to perform all three scrappings '''
    global email_checked, text_checked, search_history


    if keyword[0] != '"':
        keyword = '"' + keyword + '"'


    text_scrapping(keyword)
    image_scrapping(keyword)
    youtube_scrapping(keyword)





Top = Frame(gui, width=1000,height=80)
Left = Frame(gui, width=500, height=335)
RightUp = Frame(gui, width=500, height=335)
RightBtm = Frame(gui, width=500, height=335)

do_layout()


history_launch()
instruction_launch()


Top_Frame = LabelFrame(Top, text = "Current Setting", padx = 5, pady = 5)
Top_Frame.pack(expand = 1,fill = "both", padx = 10, pady = 10)

keyword_prompt = Label(Top_Frame, text="Please enter your keyword: ")
keyword_prompt.grid(row = 0, column = 0)
keyword_entry = Entry(Top_Frame, width = 35)
keyword_entry.grid(row = 0, column = 1)
Start_Search = Button(Top_Frame, text = "Start", command = lambda:web_scrapping(keyword_entry.get()))
Start_Search.grid(row = 0, column = 2, padx = 5)



my_menu = Menu(gui)
gui.config(menu = my_menu)

option_menu = Menu(my_menu)
my_menu.add_cascade(label="Option", menu=option_menu)
option_menu.add_command(label="Keywords", command=  keyword_popup)
option_menu.add_separator()
option_menu.add_command(label="Frequency", command=  frequency_popup)
option_menu.add_separator()
option_menu.add_command(label="Result Communication", command= result_popup)


history_menu = Menu(my_menu)
my_menu.add_cascade(label="History", menu=history_menu)
history_menu.add_command(label="History", command=  history_popup)




about_menu = Menu(my_menu)
my_menu.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="Guidelines", command=  instruction_popup)
about_menu.add_separator()
about_menu.add_command(label="About", command= lambda: placeholder("This is a webscrapping tool developed by Kevin Cheung for OSU CS361."))




gui.mainloop()

