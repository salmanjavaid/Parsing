import re
import urllib, urllib2
from multiprocessing import Pool
from bs4 import BeautifulSoup
import bleach
import MySQLdb

#content extractor function
def ret_ed_content(list_): #list of links
    for l in list_: #iterate over links
        print l
        page = BeautifulSoup(urllib.urlopen(l)) #open link
        #find the title of editorial, and then clean the tags, and extract text
        print  bleach.clean(page.findAll("h1", {"class": "story-hed"})[0], tags=[], strip=True).strip() 
        #find the story content in div
        divs = page.findAll("div", {"class": "row-fluid story-content"})
        #clean the div of tags
        k = bleach.clean(divs[0], tags=[], strip=True)
        print k
        #write to file
        text_file = open('output.txt', 'w')
        #use unicode encoding
        text_file.write(k.encode('utf-8').strip())
        #close file
        text_file.close()
        
#this is to retrieve main editorial or editorials, currently single but just to be careful for future
def ret_ed_front(divs):
    list_ = [] #generate an empty list
    for div in divs: #iterate over divs
        links = div.findAll('h2', {"class" : "story-hed"}) #find those tags with h2, and class story-hed, name is same but font is bigger for emphasis
        for l in links: #iterate over links
            list_.append(l.find('a').get('href')) #append links to list

    ret_ed_content(list_)#call the content extractor function


#this is to retrieve second editorials
def ret_ed_sec(divs):
    list_ = [] #generate an empty list
    for div in divs: #iterate our divs
        links = div.findAll('h3', {"class" : "story-hed"}) #find those tags with h3 and class story-hed
        for l in links: #iterate over links
             list_.append(l.find('a').get('href')) #links are stored in href tags, retrieve them

    ret_ed_content(list_) #send the links to editorial content function, this extract text

# this function retrieves links for editorials
def ret_ed_links(page):
    ret_ed_front(page.findAll("div", {"class": "row-fluid story story-type-newspaper-main"})) #Dawn has two editorials, main, and the second ones, this is for main
    ret_ed_sec(page.findAll("div", {"class": "row-fluid story story-type-row"})) #the second editorial

        


# driver function, currently using saved html file from folder
def demo():
#   page = urllib.urlopen('http://www.dawn.com/newspaper/editorial/2013-09-18')
    
    page = open('Test.html')  #open html file
    
    ret_ed_links(BeautifulSoup(page))  #call the editorial link function and extract links from page
    
#main
if __name__ == '__main__': 
    
    demo() #call driver function
