class Client:
    def __init__(self, id, clientName, sid):
        self.clientId: int = id
        self.clientName: str = clientName
        self.clientSid: any = sid
        #self.clientSocket: any = clientSocket
    
    # def deleteClient(sid):
    #     newClientList = [client for client in clientList if client.clientSid != sid]
    #     clientList = newClientList


clientList: Client = []