# -*- coding: utf-8 -*-
"""
Created on Sun May  6 11:59:24 2018

@author: FranchuFranchu

To use:
theotown search road
theotown download "https://theotown.com/forum/viewtopic.php?style=16&t=5776"

Enjoy


Bugs:
    Only can download plugins from direct attachment, not inline :(
"""
from urllib.request import urlopen
from html.parser import HTMLParser
from random import random
from os import remove
from kivy.utils import platform
import time
import re
def get(ls,i):
    try:
        return ls[i]
    except:
        return None
"""
 _______  _______  _        _______  _______ _________ _______  _______ 
(  ____ \(  ____ \( \      (  ____ \(  ____ \\__   __/(  ____ \(  ____ )
| (    \/| (    \/| (      | (    \/| (    \/   ) (   | (    \/| (    )|
| (_____ | (__    | |      | (__    | |         | |   | (__    | (____)|
(_____  )|  __)   | |      |  __)   | |         | |   |  __)   |     __)
      ) || (      | |      | (      | |         | |   | (      | (\ (   
/\____) || (____/\| (____/\| (____/\| (____/\   | |   | (____/\| ) \ \__
\_______)(_______/(_______/(_______/(_______/   )_(   (_______/|/   \__/
"""
class selecter(HTMLParser):
    #selects the post from all the aviable ones
    def handle_starttag(self,tag,attrs):
        try:
            self.openedLevel
        except:
            self.openedLevel = 0
        if self.openedLevel == 0:
            if tag == 'html':
                self.openedLevel +=1
                print('Scanning post...')
            self.selectedPost = False
        elif self.openedLevel == 1:
            if tag == 'body':
                self.openedLevel +=1
        elif self.openedLevel == 2:
            if get(attrs,0) == ('id','wrap'):
                self.openedLevel +=1
        elif self.openedLevel == 3:
            if get(attrs,0) == ('id','page-body'):
                self.openedLevel += 1
        elif self.openedLevel == 4:
            if not(self.selectedPost):
                err = False
                try:
                    if attrs[1][1][0:4] == 'post':
                    
                        self.openedLevel +=1
                        self.selectedPost = True
                        print(attrs)
                except IndexError:
                    pass
                if err: raise SyntaxError
        elif self.openedLevel == 5:
            if get(attrs,0) == ('class','inner'):
                self.openedLevel +=1
        elif self.openedLevel== 6:
            if get(attrs,0) == ('class','postbody'):
                self.openedLevel+=1
        elif self.openedLevel == 7:
            if 'post_content' in attrs[0][1]:
                self.openedLevel +=0.5
                print(self.getpos())
        elif self.openedLevel == 7.5:
            if get(attrs,0) == ('class','content'):
                self.openedLevel+=0.5
        elif self.openedLevel == 8:
            self.openedLevel +=1
            print(self.getpos())
            self.start = self.getpos()[1]
        elif self.openedLevel == 9:
            self.openedLevel+=1
    def handle_endtag(self,tag):
        if self.openedLevel > 9:
            self.openedLevel -= 1
        elif self.openedLevel == 9:
            self.end = self.getpos()[1]
            self.openedLevel = -1
"""
 ______   _______ _________          _______ 
(  __  \ (  ____ )\__   __/|\     /|(  ____ \
| (  \  )| (    )|   ) (   | )   ( || (    \/
| |   ) || (____)|   | |   | |   | || (__    
| |   | ||     __)   | |   ( (   ) )|  __)   
| |   ) || (\ (      | |    \ \_/ / | (      
| (__/  )| ) \ \_____) (___  \   /  | (____/\
(______/ |/   \__/\_______/   \_/   (_______/
"""
class drive(HTMLParser):
    def handle_starttag(self,tag,attrs):
        if tag == 'meta':
            if attrs[0][1] == 'og:title':
                sys.exit()
                self.saveAs = attrs[1][1]
            if attrs[0][1] == 'og:url':
                #self.saveAs = re.sub(r'[^\x00-\x7F]+','', self.saveAs)
                new = open('plugins/'+self.saveAs.replace('\\n','').replace('\\t',''),'wb')
                new.write(urlopen(attrs[1][1]).read())
                print({'fileName':self.saveAs})
                sys.exit()


"""
 _______  _______  _______  ______   _______  _______ 
(  ____ )(  ____ \(  ___  )(  __  \ (  ____ \(  ____ )
| (    )|| (    \/| (   ) || (  \  )| (    \/| (    )|
| (____)|| (__    | (___) || |   ) || (__    | (____)|
|     __)|  __)   |  ___  || |   | ||  __)   |     __)
| (\ (   | (      | (   ) || |   ) || (      | (\ (   
| ) \ \__| (____/\| )   ( || (__/  )| (____/\| ) \ \__
|/   \__/(_______/|/     \|(______/ (_______/|/   \__/
"""
class reader(HTMLParser):
    #downloads from the attachbox and inline!
    def handle_starttag(self,tag,attrs):
        try:
            self.openedLevel
        except:
            self.oopened = False
            self.openedLevel = 10
            self.dFile = False
            self.saveAs = ''
            self.aopened = False
            self.lock = False
            self.hiter = 1
        if self.openedLevel == 10:
            if tag == 'a' and 'https://drive.google.com/file/d/' in get(attrs,0)[1]:
                f = drive()
                print(attrs[0][1])
                sys.exit()
                f.feed(str(urlopen(attrs[0][1]).read()))
            if get(attrs,0) == ('class','attachbox'):
                self.openedLevel+=1
                self.inline = False
            if get(attrs,0) == ('class','inline-attachment'):
                self.openedLevel+=2
                self.inline = True
        elif self.openedLevel == 11:

            if tag == 'dd':
                self.openedLevel += 1
        elif self.openedLevel == 12:
            if self.inline:
                if tag == 'dl' and get(attrs,0) == ('class','file'):
                    self.openedLevel += 1
            elif tag == 'dl':
                self.openedLevel += 1
        elif self.openedLevel == 13:
            if tag == 'dt':
                self.openedLevel += 1
        elif self.openedLevel == 14:
            if tag == 'a':
                
                if get(get(attrs,1),1) in ['top','avatar']:
                    self.openedLevel = 10
                elif 'drive.google.com/file/d' in get(get(attrs,0),1):
                    f = drive()
                    print(attrs[0][1])
                    sys.exit()
                    f.feed(str(urlopen(attrs[0][1]).read()))
                else:
                    if platform == 'android':
                        file =open('/sdcard/TheoTown/plugins/.temp','wb')
                    else:
                        file =open('plugins/.temp','wb')
                    print('Saving...')
                    url = 'http://www.theotown.com/forum'+attrs[1][1][1:]
                    print(url)
                    bytes = urlopen(url).read()
                    self.lock = False
                    file.write(bytes)
                    file.close()
                    self.aopened = True
                    
        else:
            raise SyntaxError
        #if vap < self.openedLevel:
        #    print('good')
        #    print(vap)
    def handle_data(self,data):
        if self.openedLevel == 14:
            if self.aopened:
                self.saveAs+=data

    def handle_endtag(self,tag):
        if not(self.dFile) and tag == 'html' :
            print('Seems the creator of this plugin published this in a way we could not understand')
            raise SystemExit
        elif tag=='html':
            print('}')
        elif self.aopened and tag == 'a':
            if platform == 'android':
                file =open('/sdcard/TheoTown/plugins/.temp','rb')
            else:
                file = open('plugins/.temp','rb')
            print(self.saveAs)
            #self.saveAs = re.sub(r'[^\x00-\x7F]+','', self.saveAs)
            if platform == 'android':
                new =open('/sdcard/TheoTown/plugins/'+self.saveAs.replace('\\n','').replace('\\t',''),'wb')
            else:  
                new = open('plugins/'+self.saveAs.replace('\\n','').replace('\\t',''),'wb')
            new.write(file.read())
            file.close()
            if platform == 'android':
                remove('/sdcard/TheoTown/plugins/.temp')
            else:
                remove('plugins/.temp')
            print({'fileName':self.saveAs})
            self.dFile = True
            self.openedLevel = 10
            self.lock = False
            self.hiter = 1
            self.hiter +=11
            self.aopened = False



"""

 _______  _______  _______  _______  _______           _______  _______ 
(  ____ \(  ____ \(  ___  )(  ____ )(  ____ \|\     /|(  ____ \(  ____ )
| (    \/| (    \/| (   ) || (    )|| (    \/| )   ( || (    \/| (    )|
| (_____ | (__    | (___) || (____)|| |      | (___) || (__    | (____)|
(_____  )|  __)   |  ___  ||     __)| |      |  ___  ||  __)   |     __)
      ) || (      | (   ) || (\ (   | |      | (   ) || (      | (\ (   
/\____) || (____/\| )   ( || ) \ \__| (____/\| )   ( || (____/\| ) \ \__
\_______)(_______/|/     \||/   \__/(_______/|/     \|(_______/|/   \__/
                                                                        

"""
class searcher(HTMLParser):
    def handle_starttag(self,tag,attrs):
        #print(attrs)

        if self.openedLevel == 0:
            if tag == 'html':
                self.openedLevel +=1
            self.selectedPost = False
        elif self.openedLevel == 1:
            if tag == 'body':
                self.openedLevel +=1
        elif self.openedLevel == 2:
            if get(attrs,0) == ('id','wrap'):
                self.openedLevel +=1
        elif self.openedLevel == 3:
            if get(attrs,0) == ('id','page-body'):
                self.openedLevel += 1
        elif self.openedLevel == 4:
            if tag == 'li':
                if get(attrs,0) == ('class','arrow next'):
                    self.waitForA = True
            if self.waitForA and attrs[0] == ('class',"button button-icon-only"):
                new = self.__class__()
                new.feed(str((urlopen('http://www.theotown.com/forum'+attrs[1][1][1:]).read())))
                self.ls.extend(new.ls)
                self.waitForA = False
            if get(attrs,0) == ('class','search post bg2') or get(attrs,0) == ('class','search post bg1'):
                self.openedLevel += 1
        elif self.openedLevel == 5:
            if get(attrs,0) == ('class','inner'):
                self.openedLevel +=0.5
        elif self.openedLevel== 5.5:
            if get(attrs,0) == ('class','postbody'):
                self.openedLevel+=0.25
        elif self.openedLevel == 5.75:
            if tag == 'h3':
                self.openedLevel+=0.25
        elif self.openedLevel == 6:
            if tag == 'a':
                self.openedLevel +=1
                self.links.append('http://www.theotown.com/forum'+attrs[0][1][1:])
                self.currLink = 'http://www.theotown.com/forum'+attrs[0][1][1:]
                self.haveToRead = True
    def handle_data(self,data):
        try:
            self.openedLevel
        except:
            self.openedLevel = 0
            self.data = ''
            self.links = []
            self.ls = []
            self.pData = ''
            self.waitForA = False
        if self.openedLevel == 7:
            self.data+=(data) 
    def handle_endtag(self,tag):
        if tag == 'a' and self.openedLevel == 7:
            self.ls.append({'name':self.data,'link':self.currLink})
            self.openedLevel = 4
            self.data = ''
        if tag == 'html':
            for i in range(len(self.ls)):
                j = self.ls[i]
                self.pData+=(str(i+1)+': '+j["name"]+'\n')
"""

 ______  _______ _________ _       
(       )(  ___  )\__   __/( (    /|
| () () || (   ) |   ) (   |  \  ( |
| || || || (___) |   | |   |   \ | |
| |(_)| ||  ___  |   | |   | (\ \) |
| |   | || (   ) |   | |   | | \   |
| )   ( || )   ( |___) (___| )  \  |
|/     \||/     \|\_______/|/    )_)
                                    

"""
def search(what):
    res = 'http://www.theotown.com/forum/search.php?keywords='+what.replace(' ','+')+'&terms=all&author=&fid%5B%5D=43&sc=1&sf=titleonly&sr=posts&sk=t&sd=d&st=0&ch=300&t=0&submit=Search'
    cont = urlopen(res)
    se = searcher()
    se.feed(str(cont.read()))
    return se
def interactive():
    se = search(input('Search for: '))
    print(se.pData)
    print('Select a number: ')
    download(se.ls[int(input())-1]['link'])
def json_search(what):
    se = search(what)
    print(str(se.ls).replace("'",'"'))
    sys.exit(0)
def download(link):
    lnk = str(urlopen(link).read())
    p = selecter()
    p.feed(lnk)
    a = reader()
    a.feed(lnk[p.start:])
import sys
if __name__ == '__main__':
    try:
        action = sys.argv[1]
        count = 0
        what = ''
        for i in sys.argv:
            count+=1
            if count > 2:
                what+=(i+' ')
    except IndexError:
        action =  'i'
        #print("""You have to run this from the command line, like this:
#path/to/this/script>theotown search designate road""")
        #time.sleep(5)
        #sys.exit(3)
    if action in ['s','search']:
        what = what.replace(' ','%20')
        json_search(what)
    elif action in ['d','download']:
        download(what)
    elif action in ['i','interactive']:
        interactive()
    else:
        print('Invalid action. Options: search|download')
        sys.exit(4)

#a = downloadPlugin()
#a.feed(str(urlopen('http://www.theotown.com/forum/viewtopic.php?f=61&t=7100').read()))
            

