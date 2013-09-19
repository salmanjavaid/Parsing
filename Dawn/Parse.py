import re
import urllib, urllib2
from multiprocessing import Pool
from bs4 import BeautifulSoup
import bleach
import MySQLdb
import time

class Dawn:
    def __init__(self, Start_Date, End_Date, Date):
        self.Start_Date = Start_Date
        self.End_Date = End_Date
        self.Date = Date
    # content extractor function
    def ret_ed_content(self, list_): #list of links
        for l in list_: #iterate over links
             print l
             try:
                 page = BeautifulSoup(self.Open_Page(l)) #open link
        #find the title of editorial, and then clean the tags, and extract text
                 i = bleach.clean(page.findAll("h1", {"class": "story-hed"})[0], tags=[], strip=True).strip() 
        #find the story content in div
                 divs = page.findAll("div", {"class": "row-fluid story-content"})
        #clean the div of tags
                 k = bleach.clean(divs[0], tags=[], strip=True)
                 u = k.encode('utf-8').strip()
        #insert into database
                 self.Insert_Into_DataBase("2013-03-22", i, u)
        #write to file
                 #text_file = open('output.txt', 'w')
        #use unicode encoding
                 #text_file.write(k.encode('utf-8').strip())
        #close file
                 #text_file.close()
             except Exception as e:
                 print (e)

    # this is to retrieve main editorial or editorials, currently single but just to be careful for future
    def ret_ed_front(self, divs):
        list_ = [] #generate an empty list
        for div in divs: #iterate over divs
            links = div.findAll('h2', {"class" : "story-hed"}) #find those tags with h2, and class story-hed, name is same but font is bigger for emphasis
            for l in links: #iterate over links
                list_.append("http://www.dawn.com" + l.find('a').get('href')) #append links to list
                   
        self.ret_ed_content(list_)#call the content extractor function
    # this is to retrieve second editorials
    def ret_ed_sec(self, divs):
         list_ = [] #generate an empty list
         for div in divs: #iterate our divs
             links = div.findAll('h3', {"class" : "story-hed"}) #find those tags with h3 and class story-hed
             for l in links: #iterate over links
                 list_.append("http://www.dawn.com" + l.find('a').get('href')) #links are stored in href tags, retrieve them
                    
         self.ret_ed_content(list_) #send the links to editorial content function, this extract text         
    # this function retrieves links for editorials
    def ret_ed_links(self, page):
         self.ret_ed_front(page.findAll("div", {"class": "row-fluid story story-type-newspaper-main"})) #Dawn has two editorials, main, and the second ones
         self.ret_ed_sec(page.findAll("div", {"class": "row-fluid story story-type-row"})) #the second editorial
    #insertion into database
    def Insert_Into_DataBase(self, date, title, content):         
        #connect to database
        db = MySQLdb.connect(host="localhost", user="admin", passwd="b1admin", db="Dawn")
        with db:
            cur = db.cursor()
            #insert into database title and content with date
            cur.execute("INSERT INTO Dawn_Database (publish_date, title, content) VALUES (%s, %s, %s)", (date, title, content))
    
        db.close()
    # retrieve from database
    def Retrieve_From_Database(self):
        #connect to database
        db = MySQLdb.connect(host="localhost", user="admin", passwd="b1admin", db="Dawn")
        with db:
            cur = db.cursor()            
            #retrieve data from database and print row by row
            cur.execute("Select * from Dawn_Database")
            rows = cur.fetchall()
            for row in rows:
                print row

        db.close()

    # Open page
    def Open_Page(self, link):
        # request page
        request = urllib2.Request(link)
        # add header to request
        request.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
        # open page
        page = urllib2.urlopen(request)
        # return the page to calling function
        return page 
    # driver function
    def demo(self):
        try:       
            # open page
            page = self.Open_Page('http://www.dawn.com/newspaper/editorial/' + self.Date)
            self.ret_ed_links(BeautifulSoup(page))  #call the editorial link function and extract links from page
        except Exception as e:
            print (e)

  
         
#main
if __name__ == '__main__': 

    d = Dawn('2013-09-10', '2013-09-10', '2013-09-12')
    d.demo()    




