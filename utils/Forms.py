import npyscreen
import pafy
from time import sleep
from googleapiclient.discovery import build

from tools.config import (
    listid,
    listtitle,
    listurl,
    url,
    idvalue,
    inputsearch,
    home
)
from utils.Buttons import (
    Searchbutton,
    Exitbutton,
    Backbutton,
    Downloadbutton,
    Playbutton
)

from tools.settings import APIkey, u

youtube = build('youtube','v3',developerKey = APIkey)

import logging
logging.basicConfig(filename='logs/log_files.log',level=logging.DEBUG)


class Search(npyscreen.FormBaseNew):

    def create(self):
        self.input = self.add(npyscreen.TitleText, name='Enter here', color="LABEL")
        self.nextrely += 2
        self.searchbutton = self.add(Searchbutton, name="SEARCH", relx=20)
        self.nextrely += -1
        self.exitbutton = self.add(Exitbutton, name="Exit", relx=20, rely=0)

    def afterEditing(self):
        try:
            logging.debug('Yayay Jayati')
            global inputsearch, listid, listtitle, listurl
            inputsearch = self.input.value
            logging.debug(inputsearch)
            # req = youtube.search().list(part ='snippet',q = inputsearch,type='video', maxResults= 1) 
            # res = req.execute()
            import json
            with open('mock-data/search_results.json', 'r') as f:
                res = json.load(f)
            for i in res['items']:
                listid.append(i['id']['videoId'])
                logging.debug(i['id']['videoId'])
                # print (i)
            logging.warning(listid[0])

            for i in listid:
                temp_url = u + i
                listurl.append(temp_url)
                logging.debug(temp_url)

                # print (i)
            for i in listurl:
                video = pafy.new(i)
                listtitle.append(video.title)
                logging.debug(video.title)
                # print (i)
            self.parentApp.switchForm('display')
            data_dict = {
                'inputsearch' : inputsearch,
                'listid' : listid,
                'listtitle' : listtitle,
                'listurl' : listurl,
            }
            with open('logs/video-details.json','w') as f:
                json.dump(data_dict,f)
        except Exception as e:
            logging.warning(e)
                


class displaydetailed(npyscreen.FormBaseNew): #detailed

    def create(self):
        pass

    def afterEditing(self):
        self.parentApp.setNextForm(None)



class displayfeed(npyscreen.FormBaseNew):  #display

    def create(self):
        import json
        logging.debug('hshshsh')
        with open('logs/video-details.json','r') as f:
            vl = json.load(f)
        logging.warning(vl)
        # logging.warning(listtitle[0])
        self.add(select,name="SEARCH RESULTS", value =vl['listtitle'], show_scroll= True)
        self.add(Exitbutton, name = "EXIT",rely=0, relx = 50, color = "CAUTIONHL")
        self.add(Backbutton, name = "BACK", rely=0, relx= 100, color="CAUTIONHL")





class select(npyscreen.MultiLineAction):

    def display_value(self, vl):
        # logging.debug(vl)
        return vl

    def actionHighlighted(self, act_on_this, key_press):

        try:

            logger.debug('here')
            # global listid, listtitle, listurl, idvalue, url
            logging.debug(act_on_this)
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

        except Exception as e:
            logging.warning(e)

class downloading(npyscreen.FormBaseNew):
    def create(self):
        try:

            self.display = self.add(npyscreen.TitleText, name =" ", value = "...DOWNLOADING...This may take a while", color="DANGER",editable= False)

            video = pafy.new(url)

            stream = video.getbest(preftype= "mp4",ftypestrict= True)

            downloads= home + "/Downloads/" + video.title + "." + stream.extension   # file path

            stream.download(filepath= downloads)

        except Exception as e:
            logging.warning(e)

    def afterEditing(self):
        npyscreen.notify_wait('Downloaded Successfully')
        self.parentApp.switchForm('MAIN')

class playing(npyscreen.FormBaseNew):
    def create(self):
        pass

    def afterEditing(self):
        pass            

