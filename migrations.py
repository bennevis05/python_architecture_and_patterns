import sqlite3


def make_migrations():
    con = sqlite3.connect('portal_database.sqlite')
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS categories 
                      (name TEXT)
                   """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS courses 
                      (name TEXT,
                       category TEXT,
                       price INTEGER,
                       course_type TEXT,
                       FOREIGN KEY(category) REFERENCES categories(name))
                   """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS users 
                      (name TEXT,
                       surname TEXT,
                       email TEXT,
                       city TEXT,
                       state TEXT)
                    """)
    con.close()
