import re
import urllib, urllib2
from multiprocessing import Pool
from bs4 import BeautifulSoup
import bleach

def ret_ed_content(list_):
    for l in list_:
        page = BeautifulSoup(urllib.urlopen(l))
        print  bleach.clean(page.findAll("h1", {"class": "story-hed"})[0], tags=[], strip=True).strip()
        divs = page.findAll("div", {"class": "row-fluid story-content"})
        k = bleach.clean(divs[0], tags=[], strip=True)
        text_file = open('output.txt', 'w')
        text_file.write(k.strip())
        text_file.close()
        

def ret_ed_links(page):
    list_ = []
    divs = page.findAll("div", {"class": "row-fluid story story-type-row"})
    for div in divs:
        links = div.findAll('h3', {"class" : "story-hed"})
        for l in links:
             list_.append(l.find('a').get('href'))
    
    ret_ed_content(list_)
        

def demo():
    ###page = urllib.urlopen('http://www.dawn.com/newspaper/editorial/2011-05-03')
    page = open('test.html')
    ret_ed_links(BeautifulSoup(page))
    

if __name__ == '__main__': 
    demo()
