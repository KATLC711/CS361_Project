from tkinter import *
from PIL import ImageTk, Image
from urllib.request import Request, urlopen
import io
import json


import socket

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
        elif check == True:
            temp = temp + response[cnt]

        cnt += 1

    return urls


s = socket.socket()
port = 12345
s.connect((socket.gethostname(), port))

# Sends request and receives response
keyword = "Biden"
image_send_request(keyword, s)
urls = image_recv_response(s)





root = Tk()
root.title('Codemy.com Image Viewer')

image_list = []

for link in urls:
    #print(link)
    image_list.append(ImageTk.PhotoImage(Image.open(io.BytesIO(urlopen(link).read())).resize((350, 300), Image.ANTIALIAS)))


my_label = Label(image=image_list[0])
my_label.grid(row=0, column=0, columnspan=3)


def forward(image_number):
    global my_label
    global button_forward
    global button_back

    my_label.grid_forget()
    my_label = Label(image=image_list[image_number - 1])
    button_forward = Button(root, text=">>", command=lambda: forward(image_number + 1))
    button_back = Button(root, text="<<", command=lambda: back(image_number - 1))

    if image_number == 5:
        button_forward = Button(root, text=">>", state=DISABLED)

    my_label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)


def back(image_number):
    global my_label
    global button_forward
    global button_back

    my_label.grid_forget()
    my_label = Label(image=image_list[image_number - 1])
    button_forward = Button(root, text=">>", command=lambda: forward(image_number + 1))
    button_back = Button(root, text="<<", command=lambda: back(image_number - 1))

    if image_number == 1:
        button_back = Button(root, text="<<", state=DISABLED)

    my_label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)


button_back = Button(root, text="<<", command=back, state=DISABLED)
button_exit = Button(root, text="Exit Program", command=root.quit)
button_forward = Button(root, text=">>", command=lambda: forward(2))

button_back.grid(row=1, column=0)
button_exit.grid(row=1, column=1)
button_forward.grid(row=1, column=2)

root.mainloop()