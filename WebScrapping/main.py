'''
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests

keywords = "corgi"

root = "https://www.google.com/search?q=trump"
link = "https://www.google.com/search?q=" + keywords + "&rlz=1C1GCEU_enUS938US938&sxsrf=AOaemvIfZ0uZWtBAmE29gEZrXAI3986tSg:1635022491397&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjFjLK2teHzAhV6nGoFHVoKBW8Q_AUoAXoECAEQAw&biw=1920&bih=969&dpr=1"
print(link)

req = Request(link, headers = {'User-Agent' : 'Mozilla/5.0'})
webpage = urlopen(req).read()

with requests.Session() as c:
    soup = BeautifulSoup(webpage, 'html5lib')
    #print(soup)

    for item in soup.find_all('div',attrs = {'class':'ZINbbc xpd O9g5cc uUPGi'}):
        #print(item)

        title = item.find('div',attrs = {'class' : 'BNeawe vvjwJb AP7Wnd'}).get_text()
        print(title)
        raw_link = item.find('a', href = True)['href']
        link = (raw_link.split("/url?q=")[1]).split('&sa=U&')[0]
        print(link)
        raw_description = item.find('div',attrs = {'class' : 'BNeawe s3v9rd AP7Wnd'}).get_text()
        description = raw_description.split(" · ")[1]
        print(description)
'''



'''
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests

keywords = "trump"

#root = "https://www.bing.com/"
link = "https://www.bing.com/news/search?q=trump&FORM=HDRSC6"
#print(link)

req = Request(link, headers = {'User-Agent' : 'Mozilla/5.0'})
webpage = urlopen(req).read()

with requests.Session() as c:
    soup = BeautifulSoup(webpage, 'html5lib')
    #print(soup)
    for item in soup.find_all('div', attrs={'class': 'news-card newsitem cardcommon b_cards2'}):
        #print(item)


        title = item.get_text()
        print(title)
        link = item['url']
        print(link)
        description = item.find_all('div', attrs={'class': 'snippet'})[0]['title']
        print(description)


'''


