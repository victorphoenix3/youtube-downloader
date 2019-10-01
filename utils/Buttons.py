import npyscreen
import sys

class Searchbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        # npyscreen.notify_wait("Searching! Please Wait!!")
        self.parent.parentApp.switchForm('display')

class Exitbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.setNextForm(None)
        npyscreen.notify_wait("Goodbye!")
        sys.exit(0)

class Backbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm('MAIN')

class Downloadbutton(npyscreen.ButtonPress):
    def whenPressed(self):
        self.parent.parentApp.switchForm('downloading') 

class Playbutton(npyscreen.ButtonPress): #incomplete
    def whenPressed(self):
        self.parent.parentApp.switchForm('playing')
