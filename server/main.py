#################################
#   uvicorn main:app --reload   #
#################################

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sockio import sio_app
import sqlite3
from sqlite3 import Error

app = FastAPI()
app.mount('/', app=sio_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def prepare_tables():
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""
    
    return sql_create_projects_table, sql_create_tasks_table

def create_project(conn, project):
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid
    
if __name__ == '__main__':
    database = r"..\database\communiator.db"
    create_table_1, create_table_2 = prepare_tables()
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, create_table_1)
        create_table(conn, create_table_2)
        project = ('Test', '2023-08-02', '2023-08-03')
        project_id = create_project(conn, project)
    else:
        print("Error! cannot create the database connection.")

    uvicorn.run('main:app', reload=True)
