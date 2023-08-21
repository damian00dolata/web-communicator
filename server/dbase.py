import sqlite3
from sqlite3 import Error

class Database:
  def __init__(self) -> None:
    database = r"..\database\communiator.db"
    create_table_1, create_table_2, create_table_3 = self.prepare_tables()
    self.conn = self.create_connection(database)
    if self.conn is not None:
      self.create_table(self.conn, create_table_1)
      self.create_table(self.conn, create_table_2)
      self.create_table(self.conn, create_table_3)
      self.logoutUsers(self.conn)
    else:
      print("Error! cannot create the database connection.")

  def create_connection(self, db_file):
    conn = None
    try:
      conn = sqlite3.connect(db_file)
      return conn
    except Error as e:
      print(e)
    return conn

  def create_table(self, conn, create_table_sql):
    try:
      c = conn.cursor()
      c.execute(create_table_sql)
    except Error as e:
      print(e)

  def prepare_tables(self):
    sql_create_rooms_table = """ CREATE TABLE IF NOT EXISTS rooms (
                                        id integer PRIMARY KEY,
                                        roomId text,
                                        name text,
                                        maxUsers integer,
                                        isTemporary integer
                                      ); """
    sql_create_messages_table = """CREATE TABLE IF NOT EXISTS messages (
                                      id integer PRIMARY KEY,
                                      clientName text,
                                      message text,
                                      roomId integer,
                                      date timestamp,
                                      FOREIGN KEY (roomId) REFERENCES rooms (id)
                                );"""
    
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                  id integer PRIMARY KEY,
                                  username text,
                                  email text,
                                  password text,
                                  isLogged integer
                            );"""
    
    return sql_create_rooms_table, sql_create_messages_table, sql_create_users_table
   
  def logoutUsers(self, conn):
    cur = conn.cursor()
    sql = ''' UPDATE users
              SET isLogged=0 '''
    cur.execute(sql)
    conn.commit()