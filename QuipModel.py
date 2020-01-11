from tinydb import TinyDB, Query

class QuipModel:
    def __init__(self, db=None, title=None, date=None, contents=None, tags=None):
        self.db = db
        self.tags = tags
        self.date = date
        self.title = title
        self.contents = contents
        self.id = self.getID()

    def save(self):
        self.db.insert({'id': self.id, 'title': self.title, 'date': self.date, 'contents': self.contents, 'tags': self.tags})

    def delete(self):
        pass

    def getID(self):
        id = 1
        flag = True
        idCheck = Query()

        while flag:
            if self.db.search(idCheck.id == id):
                id+=1
            else:
                flag = False
        print("Saving Quip With ID {}".format(id))

        return id
