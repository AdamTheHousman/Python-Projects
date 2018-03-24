import requests
import pickle
import re
from bs4 import BeautifulSoup

#function for obtaining links
def getLinks(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,"lxml")
    links = []
    for link in soup.find_all('a', href = True):
        links.append(link['href'])
    return links
    
#function for obtaining image captions
def getCaptions(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,"lxml")
    html = soup.find_all('td', {'class': "photocaption"})
    text = []
    for item in html:
        test = re.split('photocaption', str(item))
        for part in test:
            if part.count('</td>') == 1 and re.search('scope=',part) and part.count('class=') == 0:
                if part not in text:
                    text.append(part)
    captions = []
    for item in text:
        test = re.search('>(.*)<', str(item))
        captions.append(test.group(1))
    return captions
    
#function for obataining link date
global months
months = ['January','February','March','April','May','June','July','August','September','October','November','December']
def getDate(url):
    global months
    date = ""
    page = requests.get(url)
    soup = BeautifulSoup(page.text,"lxml")
    text = soup.find('div', {'class': "panel-pane pane-node-created"})
    test = re.split('\s+', str(text))
    for item in test:
        if item in months:
            date = item
    return date

#main
pages = []
url = 'http://www.newyorksocialdiary.com/party-pictures'
links = getLinks(url)

#loop to aquire just the page links
for link in links:
    if re.search('page=',link):
        if link not in pages:
            pages.append(link)
            
#remove page links from main links
links = [item for item in links if item not in pages]

#traverse through each page and aquire new links
for page in pages:
    url = 'http://www.newyorksocialdiary.com' + page
    tempLinks = getLinks(url)
    for link in tempLinks:
        if re.search('page=',link):
            if link not in pages:
                pages.append(link)
        else:
            if link not in links:
                links.append(link)
                
#remove useless links from main links
tempLinks = []
for link in links:
    if re.search("/party-pictures/",link):
        tempLinks.append(link)
links = tempLinks
                
#remove links newer than 2014
tempLinks = []
links2014= []
for link in links:
    if re.search('2015',link) or re.search('2016',link) or re.search('2017',link) or re.search('2018',link):
        tempLinks.append(link)
    if re.search('2014',link):
        links2014.append(link)
links = [item for item in links if item not in tempLinks]

#remove December 2014 links
tempLinks = []
for link in links2014:
    url = 'http://www.newyorksocialdiary.com' + link
    if getDate(url) == 'December':
        tempLinks.append(link)
links = [item for item in links if item not in tempLinks]

#traverse through each party link and get image captions
captions = []
for link in links:
    url = 'http://www.newyorksocialdiary.com' + link
    captions.extend(getCaptions(url))
    
#pickle found captions
pickle.dump(captions, open("save.p","wb"))

#print(links)
#print(pages)