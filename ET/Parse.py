import re
import urllib, urllib2
from multiprocessing import Pool
from bs4 import BeautifulSoup
import bleach
import MySQLdb
import datetime

class ET:
    def __init__(self, Page_No):
        self.Page_No = Page_No
    # content extractor function
    def ret_ed_content(self, list_): #list of links
        for l in list_: #iterate over links
             try:
                 page = BeautifulSoup(self.Open_Page(l)) #open link
        #find the title and date of editorial, and then clean the tags, and extract text
                 title = bleach.clean(page.findAll("h1", {"class": "title"})[0], tags=[], strip=True).strip().encode('utf-8')
                 date = bleach.clean(page.findAll("div", {"class": "timestamp"})[0], tags=[], strip=True).strip().encode('utf-8')              
        # date is in September 20, 1993 format so convert it to Year-Month-Day format to ensure consistency
                 date = datetime.datetime.strptime(date.split(':')[1].strip(), '%B %d, %Y').strftime('%Y-%m-%d')
        #find the story content in div
                 divs = page.find("div", {"class": "clearfix story-content"}).findAll('p', {"class": ""})
                 content =  bleach.clean(divs, tags=[], strip=True).strip().encode('utf-8')    
        #insert into database
                 self.Insert_Into_DataBase(date, title, content)
             except Exception as e:
                 print (e)
    #insertion into database
    def Insert_Into_DataBase(self, date, title, content):         
        #connect to database
        db = MySQLdb.connect(host="localhost", user="admin", passwd="b1admin", db="ET")
        with db:
            cur = db.cursor()
            #insert into database title and content with date
            cur.execute("INSERT INTO ET_Database (publish_date, title, content) VALUES (%s, %s, %s)", (date, title, content))
    
        db.close()
    # retrieve from database
    def Retrieve_From_Database(self):
        #connect to database
        db = MySQLdb.connect(host="localhost", user="admin", passwd="b1admin", db="ET")
        with db:
            cur = db.cursor()            
            #retrieve data from database and print row by row
            cur.execute("Select * from ET_Database")
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
    # retrieve divs in pages
    def ret_divs(self, page):
        return page.findAll("div", {"class": "story  cat-0 group-0 position-0 couplet clearfix"})
    # retrieve links in divs for editorial links
    def ret_links(self, divs):
        list_ = []  #list to store links
        for div in divs: #iterate over divs
            links = div.findAll('h2', {"class" : "title"}) #links are stored in h2 tag with class title
            for l in links: #iterate over links
                 list_.append(l.find('a').get('href')) #append lists with links
        return list_
    # debuggin module to print links
    def Print_Links(self, list_):
        for l in list_: #iterate over list of links and print
            print l
    # driver function
    def demo(self):
        try:       
            # open page
            page = self.Open_Page('http://tribune.com.pk/author/79/editorial')
            self.ret_ed_content(self.ret_links(self.ret_divs(BeautifulSoup(page))))  #call the editorial link function and extract links from page
        except Exception as e:
            print (e)
 
         
#main
if __name__ == '__main__': 
 
    d = ET(1)
    d.demo()    




