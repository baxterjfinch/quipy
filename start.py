import json
import os.path
import datetime
from io import StringIO
from textwrap import wrap
from QuipModel import QuipModel
from tinydb import TinyDB, Query
from colorclass import Color, Windows
from terminaltables import SingleTable

class Quipy:
    ### Quipy constructor method ###
    def __init__(self, selectedDB=None):
        if selectedDB == "main":
            self.db = TinyDB('main.json')
        elif selectedDB == "secondary":
            self.db = TinyDB('secondary.json')
        else:
            self.db = TinyDB('db.json')
            #self.whatever = "string of whatever"

    ### Quip-specific functions: New, Delete, Get one, Get multi ###
    def NewQuip(self):
        title = input("\nTitle: ")
        contents = input("\n\nContents: \n\n")
        tags = self.createTagsList()
        date = str(datetime.date.today())
        newQuip = QuipModel(db=self.db, title=title, date=date, contents=contents, tags=tags)
        newQuip.save()

    def DeleteQuip(self):
        id = input("ID: ")
        quip = Query()
        print("\n\nDELETING QUIP {}\n\n".format(id))
        self.db.remove(quip.id == int(id))

    def GetQuip(self):
        id = input("ID: ")
        quip = Query()
        print("\n\nGETTING QUIP {}\n\n".format(id))

        thisQuip = self.db.search(quip.id == int(id))[0]
        quipio = StringIO()
        json.dump(thisQuip, quipio)

        print(self.buildQuipTable(quipio.getvalue()))

    def GetQuips(self):
        table_title = "Library"
        table_data = ()
        quips = self.db.all()

        for quip in quips:
            quipio = StringIO()
            json.dump(quip, quipio)
            quip = json.loads(quipio.getvalue())
            title = quip["title"]
            id = quip["id"]
            date = quip["date"]
            table_data =  ((id, date, title),) + table_data

        table_data = (('ID', 'Date', 'Title'),) + table_data
        table_instance = SingleTable(table_data, table_title)
        table_instance.justify_columns[2] = 'left'

        print("\n")
        print(table_instance.table)
        print()

    ### Helper functions related to structure and/or funcitonality (MainMenu) ###
    def buildQuipTable(self, quip):
        tags = ''
        quip = json.loads(quip)

        for tag in quip['tags']:
            tag += ' '
            tags += tag

        table_data = [
            [Color("TAGS\n{}".format(tags)), ''],
        ]

        table = SingleTable(table_data, "(ID: {}) {} -- {}".format(quip['id'], quip['title'], quip['date']))
        max_width = table.column_max_width(1)
        wrapped_string = '\n'.join(wrap(quip['contents'], max_width))
        table.table_data[0][1] = wrapped_string

        return(table.table)

    def createTagsList(self):
        tags = []
        adding = True
        print("\n\nAdd as many tags as you want. Press Enter after each one. Type Done/done/d when you are finished...\n")

        while adding:
            tag = input("\nAdd A Tag: ")
            if tag == "done" or tag == "d" or tag == "Done" or tag == "DONE":
                adding = False
                break
            else:
                tags.append(tag)

        return tags

    def MainMenu(self):
        print("\n\nWelcome to Quipy. A simple note-taking application.\nChoose an option below: \n\n")
        print("(1) Create A Quip\n(2) Get A Quip\n(3) Get All Quips\n(4) Delete A Quip\n\n")

        option = input(">>> ")
        switcher = {
            "1": self.NewQuip,
            "2": self.GetQuip,
            "3": self.GetQuips,
            "4": self.DeleteQuip
        }

        func = switcher.get(option, lambda: "Invalid Option")
        func()


qpy = Quipy("default")
qpy.MainMenu()

### Pseudo-unit tests ###

#qpy.NewQuip()
#qpy.GetQuips()
#qpy.GetQuip(1)
#qpy.DeleteQuip(3)
