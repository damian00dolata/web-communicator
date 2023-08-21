class Client:
  def __init__(self, id, clientName, sid):
    self.clientId: int = id
    self.clientName: str = clientName
    self.clientSid: any = sid

clientList: Client = []