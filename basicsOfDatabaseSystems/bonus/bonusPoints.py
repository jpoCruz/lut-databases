import sqlite3
from sqlite3 import Error
import os

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
        c = conn.cursor();
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = ("bonus.db")
    os.remove("bonus.db")

    students = ("""CREATE TABLE 'students'(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name NVARCHAR(20)  NOT NULL,
    major NVARCHAR(20)  NOT NULL,
    age INTEGER
    );""")

    books = ("""CREATE TABLE 'books'(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    title NVARCHAR(20)  NOT NULL,
    publisher NVARCHAR(20)  NOT NULL,
    year NVARCHAR(4)
    );""")

    borrows = ("""CREATE TABLE 'borrows'(
    docId INTEGER REFERENCES books(id),
    stId INTEGER REFERENCES students(id),
    date DATETIME
    );""")

    conn = create_connection(database)

    if conn is not None:    # create table
        create_table(conn, students)  # create students table
        print("Created students table")
        conn.commit()
        create_table(conn, books)
        print("Created books table")     # create books table
        conn.commit()
        create_table(conn, borrows)    # create borrow table
        print("Created borrows table")
        conn.commit()
        print("Tables successfully created.")
    else:
        print("Error. Cannot create the database connection.")



    #now to populate all of them
    #populating students
    conn.execute("""INSERT INTO students (id, name, major, age)
    VALUES (0, 'Joao Paulo', 'Computer Science', 20)""")
    conn.execute("""INSERT INTO students (name, major, age)
    VALUES ('Marcel Pflugfelder', 'Industrial Engineering', 20)""")
    conn.execute("""INSERT INTO students (name, major, age)
    VALUES ('Julian Boch', 'Industrial Engineering', 21)""")
    conn.execute("""INSERT INTO students (name, major, age)
    VALUES ('Vittu Virtanen', 'Software Engineering', 23)""")
    conn.commit()
    #populating books
    conn.execute("""INSERT INTO books (id, title, publisher, year)
    VALUES (0, 'ICT Innovations for Sustainability', 'Springer', '2015')""")
    conn.execute("""INSERT INTO books (title, publisher, year)
    VALUES ('The Hobbit', 'George Allen & Unwin', '1937')""")
    conn.execute("""INSERT INTO books (title, publisher, year)
    VALUES ('Don Quixote', 'Francisco de Robles', '1605')""")
    conn.execute("""INSERT INTO books (title, publisher, year)
    VALUES ('The Little Prince', 'Reynal & Hitchcock', '1943')""")
    conn.commit()
    #populating borrows
    conn.execute("""INSERT INTO borrows (docId, stId, date)
    VALUES (0, 0, '2020-02-02')""")
    conn.execute("""INSERT INTO borrows (docId, stId, date)
    VALUES (1, 0, '2020-02-23')""")
    conn.execute("""INSERT INTO borrows (docId, stId, date)
    VALUES (0, 3, '2019-11-08')""")
    conn.execute("""INSERT INTO borrows (docId, stId, date)
    VALUES (2, 1, '2020-01-16')""")
    conn.commit()

    print("All tables successfully populated.")

if __name__ == '__main__':
    main()
