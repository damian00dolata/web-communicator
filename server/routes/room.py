from models.room import Room
import json
from fastapi import status

class RoomService:
  async def addRoom(conn, room: Room, response):
    cur = conn.cursor()
    sql = ''' SELECT roomId from rooms where roomId=? '''
    cur.execute(sql, (room.roomId,))
    exists = cur.fetchone()
    if exists:
      response.status_code = status.HTTP_409_CONFLICT
      return {"message":"Room ID already in use."}
    sql = ''' INSERT INTO rooms(roomId,name,maxUsers, isTemporary)
          VALUES(?,?,?,?) RETURNING id '''
    _room = (room.roomId, room.name, room.maxUsers, room.isTemporary)
    cur.execute(sql, _room)
    data = cur.fetchone()
    if cur.rowcount < 1:
      response.status_code = status.HTTP_409_CONFLICT
      return {"message":"Adding room unsuccessful."}
    conn.commit()
    room.id = data
    return json.dumps(room, default=lambda o: o.__dict__)

  async def removeRoom(conn, _id, response):
    sql = ''' SELECT id FROM rooms WHERE id=? '''
    cur = conn.cursor()
    cur.execute(sql, _id)
    data = cur.fetchone()
    if data:
      sql = ''' DELETE FROM rooms WHERE id=? '''
      cur.execute(sql, _id)
      conn.commit()
      return {"message":"Removing room successful."}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":"Removing room unsuccessful."}
   
  async def findById(conn, _id, response):
    sql = ''' SELECT * FROM rooms WHERE id=? '''
    cur = conn.cursor()
    cur.execute(sql, _id)
    conn.commit()
    row = cur.fetchone()
    if row:
      return json.dumps(row)
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":"Finding room by id unsuccessful."}
   
  async def findByRoomId(conn, roomId, response):
    sql = ''' SELECT * FROM rooms WHERE roomId=? '''
    cur = conn.cursor()
    cur.execute(sql, (roomId,))
    conn.commit()
    row = cur.fetchone()
    if row:
      return json.dumps(row)
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":"Finding room by room id unsuccessful."}
   
  async def getAllRooms(conn):
    sql = ''' SELECT * FROM rooms '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    rows = cur.fetchall()
    return json.dumps(rows)