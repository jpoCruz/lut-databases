import sqlite3
from sqlite3 import Error
from pprint import pprint
import os
import sys

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

def newFile(database):
    conn = create_connection(database)
    students = ("""CREATE TABLE 'students'(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    first_name NVARCHAR(32)  NOT NULL,
    last_name NVARCHAR(32)  NOT NULL,
    email NVARCHAR(64)  NOT NULL,
    course1 INTEGER NOT NULL REFERENCES courses(id),
    course2 INTEGER REFERENCES courses(id),
    course3 INTEGER REFERENCES courses(id),
    course4 INTEGER REFERENCES courses(id),
    course5 INTEGER REFERENCES courses(id),
    course6 INTEGER REFERENCES courses(id)
    );""")

    courses = ("""CREATE TABLE 'courses'(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name NVARCHAR(20)  NOT NULL,
    teacherId INTEGER NOT NULL REFERENCES teachers(id)
    );""")

    teachers = ("""CREATE TABLE 'teachers'(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    first_name NVARCHAR(32)  NOT NULL,
    last_name NVARCHAR(32)  NOT NULL,
    email NVARCHAR(64)  NOT NULL
    );""")

    # because of table references, the tables need to be created in
    # the order of teachers, then courses, and then students

    if conn is not None:    # creates all tables
        create_table(conn, teachers)        # create teachers table
        print("Created teachers table.")
        conn.commit()
        create_table(conn, courses)         # create courses table
        print("Created courses table.")
        conn.commit()
        create_table(conn, students)        # create students table
        print("Created students table.")
        conn.commit()
        print("All tables successfully created.")
    else:
        print("Error. Cannot create the database connection.")

    # tables must be populated in the same order.


    # as a default, all emails for teachers on
    # this system will be firstname.lastname@lut.fi
    #populates teachers
    conn.execute("""INSERT INTO teachers (id, first_name, last_name, email)
    VALUES (0, 'Shola', 'Oyedeji', 'shola.oyedeji@lut.fi')""")
    conn.execute("""INSERT INTO teachers (first_name, last_name, email)
    VALUES ('Antti', 'Knutas', 'antti.knutas@lut.fi')""")
    conn.execute("""INSERT INTO teachers (first_name, last_name, email)
    VALUES ('Sami', 'Jantunen', 'sami.jantunen@lut.fi')""")
    conn.execute("""INSERT INTO teachers (first_name, last_name, email)
    VALUES ('Jari', 'Porras', 'jari.porras@lut.fi')""")
    print("Teachers populated successfully.")
    conn.commit()

    #populates courses
    conn.execute("""INSERT INTO courses (id, name, teacherId)
    VALUES (0, 'Basics of Database Systems', 0)""")
    conn.execute("""INSERT INTO courses (name, teacherId)
    VALUES ('User Interfaces and Usability', 1)""")
    conn.execute("""INSERT INTO courses (name, teacherId)
    VALUES ('Project Management', 2)""")
    conn.execute("""INSERT INTO courses (name, teacherId)
    VALUES ('Sustainability and IT', 3)""")
    print("Courses populated successfully.")
    conn.commit()

    # as a default, all emails for students on
    # this system will be firstname.lastname@student.lut.fi
    #populates students
    conn.execute("""INSERT INTO students (id, first_name, last_name, email, course1, course2, course3, course4)
    VALUES (0, 'Joao', 'Cruz', 'joao.cruz@student.lut.fi', 0, 1, 2, 3)""")
    conn.execute("""INSERT INTO students (first_name, last_name, email, course1)
    VALUES ('Marcel', 'Pflugfelder', 'marcel.pflugfelder@student.lut.fi', 0)""")
    conn.execute("""INSERT INTO students (first_name, last_name, email, course1, course2)
    VALUES ('Julian', 'Boch', 'julian.boch@student.lut.fi', 0, 2)""")
    conn.execute("""INSERT INTO students (first_name, last_name, email, course1, course2, course3)
    VALUES ('Vittu', 'Virtanen', 'vittu.virtanen@student.lut.fi', 1, 2, 3)""")
    print("Students populated successfully.")
    conn.commit()

    print("Startup sequence finished. Opening database manager...")
    print("")
    menu(database)

def menu(database):
    conn = create_connection(database)
    print("---==========    MENU    ==========---")
    print("1. Insert student    2. Update student")
    print("3. Delete student    ")
    #print("5. Insert teacher    6. Update/delete teacher")
    print("4. Show students of specific course")
    print("0. Quit")

    choice = input("> ")
    choice = int(choice)
    print("")
    if choice == 1: #insert student
        command = ("""INSERT INTO students(first_name, last_name, email, course1)
        VALUES (""")
        temp_name = input("Student's first name > ")
        temp_lastname = input("Student's last name > ")
        temp_course = input("Student's course id > ")

        command+= "'"
        command+= temp_name
        command+= "', '"
        command+= temp_lastname
        command+= "', '"
        temp_email = (temp_name.lower() + '.' + temp_lastname.lower() + "@student.lut.fi', ")
        command+= temp_email
        command+= temp_course
        command+= ')'

        conn.execute(command)
        conn.commit()
        print("Successfully inserted.")
        print("")
        menu(database)

    elif choice == 2: #update student
        command = """UPDATE students
        SET course1 = """
        print("Type the ID of the student you want to update:")
        temp_id = input("> ")
        print("Warning: this will override the current course1")
        print("Type the new student course:")
        temp_course = input("> ")
        command+= temp_course
        command+= " WHERE id = "
        command+= temp_id
        command+= ';'
        
        conn.execute(command)
        conn.commit()
        print("Successfully updated.")
        print("")
        menu(database)

    elif choice == 3: #delete student
        command = """DELETE FROM students
        WHERE id = """
        print("Type the ID of the student you want to delete:")
        temp_id = input("> ")
        command+= temp_id
        command+= ';'

        conn.execute(command)
        conn.commit()
        print("Successfully deleted.")
        print("")
        menu(database)

    #elif choice == 4: #update / delete course
    #    pass
    #elif choice == 5: #insert teacher
    #    pass
    #elif choice == 6: #update / delete teacher
        pass
    elif choice == 4: #show students of specific course
        command = ("""SELECT * FROM students
        WHERE course1 = """)
        print("Type the ID of the course from which you want to see the students:")
        temp_id = input("> ")
        command += temp_id          # I don't know the order in which the user has inserted the course,
        command+= " OR course2 = "   # so I must check all 6 columns for the course id
        command += temp_id
        command+= " OR course3 = "
        command += temp_id
        command+= " OR course4 = "
        command += temp_id
        command+= " OR course5 = "
        command += temp_id
        command+= " OR course6 = "
        command += temp_id
        command+= ";"

        cursor = conn.execute(command)
        rows = cursor.fetchall()
        for row in rows:
            print (row)

        menu(database)

    elif choice == 0: #close database
        print("See you later. :)")
        sys.exit(0)

    else:    ## default ##
        print("Invalid option.")
        print("")
        menu(database)

def main():
    database = ("database.db")

    if os.path.exists("database.db"):
        print("Opening existing database.")
        menu(database)
    else:
        print("Executing clean startup sequence.")
        newFile(database)

if __name__ == '__main__':
    main()
