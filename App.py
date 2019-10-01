import npyscreen

from utils.Forms import (
    Search, 
    displayfeed,
    displaydetailed,
    downloading,
    playing 
)

class App(npyscreen.NPSAppManaged):
   def onStart(self):
       self.addForm('MAIN', Search, name='Search')
       self.addForm('display',displayfeed, name= "SEARCH RESULTS")
       self.addForm('detailed',displaydetailed, name = " ")
       self.addForm('downloading',downloading,name = " DOWNLOAD STATUS")
       self.addForm('playing',playing, name = " Playing video")

    


if __name__ == '__main__':
   Apprun = App().run()        
