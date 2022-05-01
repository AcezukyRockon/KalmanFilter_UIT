import sqlite3
import time
from sqlite3 import Error
from datetime import datetime


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def update_task(conn, task):
    sql = ''' UPDATE tasks
              SET counter = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def update_time(conn, counter):
    sql = ''' INSERT INTO trai(id, d)
              VALUES(?,datetime('now', 'localtime')); '''
    cur = conn.cursor()
    cur.execute(sql, counter)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        for i in range(0,6):
            update_task(conn, (i,1))
            update_time(conn, (i,))
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(i)
            print(current_time)
            time.sleep(1)


if __name__ == '__main__':
    main()
