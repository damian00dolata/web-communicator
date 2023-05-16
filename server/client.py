class Client:
    def __init__(self, clientName, clientSocket):
        self.clientName: str = clientName
        self.clientSocket: any = clientSocket

clientList: Client = []