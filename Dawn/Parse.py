import re
import urllib, urllib2
from multiprocessing import Pool
from bs4 import BeautifulSoup
import bleach
import MySQLdb

def ret_ed_content(list_):
    for l in list_:
        print l
        page = BeautifulSoup(urllib.urlopen(l))
        print  bleach.clean(page.findAll("h1", {"class": "story-hed"})[0], tags=[], strip=True).strip()
        divs = page.findAll("div", {"class": "row-fluid story-content"})
        k = bleach.clean(divs[0], tags=[], strip=True)
        print k
        text_file = open('output.txt', 'w')
        text_file.write(k.encode('utf-8').strip())
        text_file.close()
        
def ret_ed_front(divs):
    list_ = []
    for div in divs:
        links = div.findAll('h2', {"class" : "story-hed"})
        for l in links:
            list_.append(l.find('a').get('href'))

    ret_ed_content(list_)

def ret_ed_sec(divs):
    list_ = []
    for div in divs:
        links = div.findAll('h3', {"class" : "story-hed"})
        for l in links:
             list_.append(l.find('a').get('href'))

    ret_ed_content(list_)

def ret_ed_links(page):
    list_ = []
    ret_ed_front(page.findAll("div", {"class": "row-fluid story story-type-newspaper-main"}))
    ret_ed_sec(page.findAll("div", {"class": "row-fluid story story-type-row"}))
    #ret_ed_content(list_)
        

def demo():
#   page = urllib.urlopen('http://www.dawn.com/newspaper/editorial/2013-09-18')
    page = open('Test.html')
    ret_ed_links(BeautifulSoup(page))
    

if __name__ == '__main__': 
    demo()
