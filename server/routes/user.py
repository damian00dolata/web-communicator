from models.user import User
import json
import bcrypt
from fastapi import status

class UserService:
  async def addUser(conn, user: User, response):
    cur = conn.cursor()
    sql = ''' SELECT username FROM users WHERE username=? '''
    cur.execute(sql, (user.username,))
    exists = cur.fetchone()
    if exists:
      response.status_code = status.HTTP_409_CONFLICT
      return {"message":"Username is taken."}
    sql = ''' INSERT INTO users(username,email,password,isLogged)
          VALUES(?,?,?,?) RETURNING id '''
    password = user.password
    passwordBytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(passwordBytes, salt)
    _user = (user.username, user.email, hashedPassword, 0)
    cur.execute(sql, _user)
    data = cur.fetchone()
    if cur.rowcount < 1:
      response.status_code = status.HTTP_409_CONFLICT
      return {"message":"Adding user unsuccessful."}
    conn.commit()
    user.id = data
    user.password = ''
    return json.dumps(user, default=lambda o: o.__dict__)
   
  async def authUser(conn, user, response):
    cur = conn.cursor()
    sql = ''' SELECT username FROM users WHERE username=? '''
    cur.execute(sql, (user.username,))
    exists = cur.fetchone()
    if exists:
      sql = ''' SELECT password, isLogged, id, email FROM users WHERE username=? '''
      cur.execute(sql, (user.username,))
      password = user.password.encode('utf-8')
      res = cur.fetchone()
      dbPass = res[0]
      isLogged = res[1]
      if isLogged:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"message":"User is already logged in."}
      if bcrypt.checkpw(password, dbPass):
        user.password = ''
        user.id = res[2]
        user.email = res[3]
        response.status_code = status.HTTP_200_OK
        return json.dumps(user, default=lambda o: o.__dict__)
      response.status_code = status.HTTP_403_FORBIDDEN
      return {"message":"Incorrect login data."}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":"Username doesn't exist."}

  async def removeUser(conn, _id, response):
    sql = ''' SELECT id FROM users WHERE id=? '''
    cur = conn.cursor()
    cur.execute(sql, _id)
    data = cur.fetchone()
    if data:
      sql = ''' DELETE FROM users WHERE id=? '''
      cur.execute(sql, _id)
      conn.commit()
      return {"message":"Removing user successful."}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":"Removing user unsuccessful."}

  async def updateUser(conn, user: User, _id, response):
    sql = ''' SELECT id FROM users WHERE id=? '''
    cur = conn.cursor()
    cur.execute(sql, _id)
    data = cur.fetchone()
    if data:
      sql = ''' UPDATE users
              SET username=?, email=?, password=?
              WHERE id=? '''
      updatedUser = (user.username, user.email, user.password, _id)
      cur.execute(sql, updatedUser)
      conn.commit()
      return {"message":"Modifying user successful."}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":"Modifying user unsuccessful."}

  async def findById(conn, _id, response):
    sql = ''' SELECT id, username, email, isLogged FROM users WHERE id=? '''
    cur = conn.cursor()
    cur.execute(sql, _id)
    conn.commit()
    row = cur.fetchone()
    if row:
      return json.dumps(row)
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":"Finding user by id unsuccessful."}

  async def findByName(conn, username, response):
    sql = ''' SELECT id, username, email, isLogged FROM users WHERE username=? '''
    cur = conn.cursor()
    cur.execute(sql, (username,))
    conn.commit()
    row = cur.fetchone()
    if row:
      return json.dumps(row)
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":"Finding user by name unsuccessful."}
      
  async def getAllUsers(conn):
    sql = ''' SELECT id, username, email FROM users '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    rows = cur.fetchall()
    return json.dumps(rows)
   
  async def changeStatus(conn, _id, response):
    sql = ''' SELECT id FROM users WHERE id=? '''
    cur = conn.cursor()
    cur.execute(sql, _id)
    data = cur.fetchone()
    if data:
      sql = ''' SELECT isLogged FROM users WHERE id=? '''
      cur.execute(sql, _id)
      res = cur.fetchone()
      isLogged = 0 if res[0] == 1 else 1
      sql = ''' UPDATE users
              SET isLogged=?
              WHERE id=? '''
      cur.execute(sql, (isLogged, _id))
      conn.commit()
      return {"message":f"Changing status to {isLogged} successful."}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message":"Changing status unsuccessful."}
