import npyscreen
import pafy
from time import sleep
import config
from config import listid, listtitle, listurl, url, idvalue,inputsearch, home 
from googleapiclient.discovery import build

APIkey= "AIzaSyAFxYhBh2iUCTiK6hVq2irLcaE0LZB4OeY"

u= "https://www.youtube.com/watch?v="

youtube = build('youtube','v3',developerKey = APIkey)

req=None
res=None


class Searchbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm('display')

class Exitbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.setNextForm(None)

class Backbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm('MAIN')

class Downloadbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm('downloading') 

class Playbutton(npyscreen.ButtonPress): #incomplete
    def whenPressed(self):
        self.parent.parentApp.switchForm('playing')



class Search(npyscreen.FormBaseNew):

    def create(self):
        self.input = self.add(npyscreen.TitleText, name='Enter here', color="LABEL")
        self.nextrely += 2
        self.searchbutton= self.add(Searchbutton, name="SEARCH", relx=20)

    def afterEditing(self):
        try:
            #global config.inputsearch, config.listid, config.listtitle, config.listurl
            config.inputsearch = self.input.value
            req = youtube.search().list(part ='snippet',q = inputsearch,type='video', maxResults= 20) 
            res = req.execute()

            for i in res['items']:
                listid.append(i['id']['videoId'])

            for i in listid:
                temp_url = u + i
                listurl.append(temp_url)

            for i in listurl:
                video = pafy.new(i)
                listtitle.append(video.title)

            self.parentApp.switchForm(None)

        except Exception:
            pass    


class displaydetailed(npyscreen.FormBaseNew): #detailed

    def create(self):
        pass

    def afterEditing(self):
        self.parentApp.setNextForm(None)



class displayfeed(npyscreen.FormBaseNew):  #display

    def create(self):

        self.add(select,name="SEARCH RESULTS", value =listtitle, color= "LABEL" ,show_scroll= True)
        self.add(Exitbutton, name = "EXIT",rely=0, relx = 0, color = "CAUTIONHL")
        self.add(Backbutton, name = "BACK", rely=0, relx= 5, color="CAUTIONHL")





class select(npyscreen.MultiLineAction):

    def display_value(self, vl):
        return (vl)

    def actionHighlighted(self, act_on_this, key_press):

        try:

            
            global listid, listtitle, listurl, idvalue, url
                
            for i in range(len(listtitle) - 1):
                if config.listtitle[i] == act_on_this:
                    config.idvalue = i
                    config.url= config.listurl[i]
                    break

            self.parent.parentApp.getForm("detailed").add(npyscreen.TitleText, name=" VIDEO : ", value = act_on_this, editable=False, hidden=False)
            self.parent.parentApp.getForm("detailed").add(npyscreen.TitleText, name=" URL : ", value = url, editable=False)
            self.parent.parentApp.getForm("detailed").add(npyscreen.TitleText, name=" DURATION : ",value= pafy.new(url).duration ,editable=False)

            self.parent.parentApp.getForm("detailed").add(Downloadbutton, name= " Click for Download ", color ="CAUTIONHL",relx=10)
            self.parent.parentApp.getForm("detailed").nextrely -=1
            self.parent.parentApp.getForm("detailed").add(Playbutton, name=" Play Now ",color = "CAUTIONHL", relx=15)

        except Exception:
            pass   

class downloading(npyscreen.FormBaseNew):
    def create(self):
        try:

            self.display = self.add(npyscreen.TitleText, name =" ", value = "...DOWNLOADING...This may take a while", color="DANGER",editable= False)

            video = pafy.new(url)

            stream = video.getbest(preftype= "mp4",ftypestrict= True)

            downloads= home + "/Downloads/" + video.title + "." + stream.extension   # file path

            stream.download(filepath= downloads)

        except Exception:
            pass

    def afterEditing(self):
        npyscreen.notify_wait('Downloaded Successfully')
        self.parentApp.switchForm('MAIN')

class playing(npyscreen.FormBaseNew):
    def create(self):
        pass

    def afterEditing(self):
        pass            


class App(npyscreen.NPSAppManaged):
   def onStart(self):
       self.addForm('MAIN', Search, name='Search')
       self.addForm('display',displayfeed, name= "SEARCH RESULTS")
       self.addForm('detailed',displaydetailed, name = " ")
       self.addForm('downloading',downloading,name = " DOWNLOAD STATUS")
       self.addForm('playing',playing, name = " Playing video")

    


if __name__ == '__main__':
   Apprun = App().run()        












        


        
