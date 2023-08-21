from models.message import Message
import datetime
from fastapi import status
import json

class MessageService:
  async def addMessage(conn, message: Message, response):
    currentDateTime = datetime.datetime.now()
    message.date = currentDateTime.strftime("%Y-%m-%d %H:%M:%S")
    sql = ''' INSERT INTO messages(clientName,message,roomId,date)
          VALUES(?,?,?,?) RETURNING id'''
    cur = conn.cursor()
    _mess = (message.clientName, message.message, message.roomId, currentDateTime.strftime("%Y-%m-%d %H:%M:%S"))
    cur.execute(sql, _mess)
    data = cur.fetchone()
    if cur.rowcount < 1:
      response.status_code = status.HTTP_409_CONFLICT
      return {"message":"Adding user unsuccessful."}
    conn.commit()
    message.id = data
    return json.dumps(message, default=json_default)

  async def getAllMessages(conn, _id):
    cur = conn.cursor()
    sql = ''' SELECT clientName, message, date FROM messages WHERE roomId=? '''
    cur.execute(sql, (_id,))
    conn.commit()
    rows = cur.fetchall()
    return json.dumps(rows)
   
  async def removeMessages(conn, roomId, response):
    sql = ''' SELECT id FROM rooms WHERE roomId=? '''
    cur = conn.cursor()
    cur.execute(sql, (roomId,))
    data = cur.fetchone()
    if data:
      sql = ''' DELETE FROM messages WHERE roomId=? '''
      cur.execute(sql, (roomId,))
      conn.commit()
      return {"message":"Removing messages successful."}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":"Removing messages unsuccessful."}
   
def json_default(value):
  if isinstance(value, datetime.date):
    return value.strftime("%Y-%m-%d %H:%M:%S")
  else:
    return value.__dict__