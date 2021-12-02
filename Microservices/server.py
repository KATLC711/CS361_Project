import socket
import json


from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import webbrowser


HEADERSIZE = 10



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(20)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")




    keyword = clientsocket.recv(1024).decode("utf-8")

    keyword = keyword.replace(" ", "%20")


    link = "https://www.google.com/search?q=" + keyword + "&rlz=1C1GCEU_enUS938US938&sxsrf=AOaemvIfZ0uZWtBAmE29gEZrXAI3986tSg:1635022491397&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjFjLK2teHzAhV6nGoFHVoKBW8Q_AUoAXoECAEQAw&biw=1920&bih=969&dpr=1"

    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()

    d = {'title': [], 'link': [], 'description': [], "search_pf": []}


    with requests.Session() as c:
        soup = BeautifulSoup(webpage, 'html5lib')



        for item in soup.find_all('div', attrs={'class': 'ZINbbc xpd O9g5cc uUPGi'}):
            title = item.find('div', attrs={'class': 'BNeawe vvjwJb AP7Wnd'}).get_text()

            d["title"].append(title)

            raw_link = item.find('a', href=True)['href']
            link = (raw_link.split("/url?q=")[1]).split('&sa=U&')[0]
         
            d["link"].append(link)

            raw_description = item.find('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'}).get_text()
            description = raw_description.split(" · ")[1]
           
            d["description"].append(description)

            d["search_pf"].append('Google')


    link = "https://www.bing.com/news/search?q=" + keyword + '&FORM=HDRSC6'

    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    with requests.Session() as c:
        soup = BeautifulSoup(webpage, 'html5lib')
        
        for item in soup.find_all('div', attrs={'class': 'news-card newsitem cardcommon b_cards2'}):

            title = item.get_text()
            d["title"].append(title)

            link = item['url']
            d["link"].append(link)

            description = item.find_all('div', attrs={'class': 'snippet'})[0]['title']
            d["description"].append(description)

            d["search_pf"].append('Bing')



    msg = json.dumps(d)

    msg = f'{len(msg):<{HEADERSIZE}}' + msg

    clientsocket.send(bytes(msg, "utf-8"))



