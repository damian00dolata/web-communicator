import datetime

class Message:
    def __init__(self, clientName, message):
        self.clientName: str = clientName
        self.message: str = message
        #self.date: datetime = datetime.datetime.now()
