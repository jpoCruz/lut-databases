import sqlite3
from sqlite3 import Error
import random
 
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
 
def string_generator(lastNameList, firstNameList, titleList, addressList, cityList, i):
    baseCommand = ("""INSERT INTO employees (lastName, firstName, title, reportsTo, address, city, country, phone, email)
    VALUES (""")
    
    command = baseCommand
    tempLastName = random.choice(lastNameList)  #adds last name
    command+= tempLastName
    command+= ", "
    tempFirstName = random.choice(firstNameList)#adds first name
    command+= tempFirstName
    command+= ", "
    command+= random.choice(titleList)  #adds title
    command+= ", "
    command+= str(random.randint(0, i)) #reportsTo can only refer to an ID already on the table, so it runs from 0 to i-1, i being the number of currently inserted employees
    command+= ", "
    command+= random.choice(addressList)#adds a random address
    tempNum = str(random.randint(0, 100))
    tempNum+= "', "
    command+= tempNum   #adds a number from 0 to 99 into the address
    command+= random.choice(cityList) #adds a random city
    command+= ", 'Finland', " #country is always Finland
        
    phoneNum = "'04"
    phoneNum += str(random.randint(0, 9)) #adds an extra digit to the 04 in the beginning of all phone numbers
    phoneNum += " "
    phoneNum += str(random.randint(100, 999)) #adds a 3 digit number
    phoneNum += " "
    phoneNum += str(random.randint(1000, 9999))#adds a 4 digit number
    command+= phoneNum
    command+= "', "
        
    tempLastName = tempLastName.lower()     #for the email, makes last name all lowercase
    tempFirstName = tempFirstName.lower()   #for the email, makes the first name all lowercase
    tempLastName = tempLastName.translate({39: None})   #removes the apostrophes from the last name
    tempFirstName = tempFirstName.translate({39: None}) #removes the apostrophes from the first name
    tempEmail = "'"
    tempEmail+= tempFirstName
    tempEmail+= '.'
    tempEmail+= tempLastName
    tempEmail+= "@company.fi')" #email = 'firstname.lastname@company.fi'
    command+= tempEmail
    
    return command
 
def main():
    database = ("week7.db")
    
    #all lists already have the apostrophes, this way SQLite knows they are TEXT
 
    lastNameList = ["'Jones'", "'Smith'", "'Davis'", "'Miller'", "'Moore'", "'Wilson'", "'Jackson'", "'White'", "'Harris'", "'Garcia'", "'Lee'", "'Walker'", "'Thompson'", "'Lopez'", "'Campbell'", "'Collins'", "'Green'", "'Hill'", "'Reed'", "'Bell'", "'Gray'", "'Cox'", "'Brooks'", "'Ward'", "'Sanders'", "'Wood'", "'Long'", "'Myers'", "'Ford'", "'West'", "'Reynolds'", "'Owens'", "'Cruz'", "'Hunter'", "'Freeman'", "'Palmer'", "'Aalto'", "'Couri'", "'Virtanen'", "'Halko'", "'Kauppi'", "'Jarvinen'", "'Laakso'", "'Kotila'", "'Kivi'"]
    
    firstNameList = ["'Alex'", "'James'", "'John'", "'Robert'", "'Thomas'", "'Daniel'", "'Linda'", "'Mary'", "'Elizabeth'", "'Sarah'", "'Lisa'", "'Betty'", "'Ashley'", "'Carol'", "'Edward'", "'Mark'", "'Ryan'", "'Eric'", "'Laura'", "'Rebecca'", "'Helen'", "'Amy'", "'Ronald'", "'Justin'", "'Nicole'", "'Anna'", "'Emma'", "'Lucas'", "'Jerry'", "'Jose'", "'Joyce'", "'Julia'", "'Maria'", "'Adam'", "'Kyle'", "'Zachary'", "'Olivia'", "'Ethan'", "'Alan'", "'Dylan'", "'Grace'", "'Denise'", "'Amber'", "'Rose'", "'Diana'", "'Natalie'", "'Judy'", "'Morgan'", "'Antti'", "'Samu'", "'Jaakko'", "'Joona'", "'Frans'", "'Zack'", "'Miika'", "'Emilia'", "'Anni'", "'Veera'", "'Oona'", "'Inka'"]
    
    titleList = ["'Manager'", "'Supervisor'", "'Employee'", "'Employee'", "'Employee'", "'Employee'", "'Employee'", "'Employee'", "'Employee'", "'Employee'"]
    
    addressList = ["'Ruskonlahdenkatu ", "'Karankokatu ", "'Keskiortentie ", "'Hakulintie ", "'Lonnrotinkatu ", "'Kaarrostie ", "'Kaarikatu ", "'Puutarhakatu ", "'Harjukuja ", "'Koskikatu ", "'Rauhankatu ", "'Liisankatu ", "'Ysitie ", "'Rauhankatu ", "'Rengaskuja "]
    
    cityList = ["'Lappeenranta'", "'Helsinki'", "'Tampere'", "'Vantaa'", "'Oulu'", "'Turku'", "'Heinola'", "'Rovaniemi'"]
 
    sql_create_table = ("""CREATE TABLE 'employees'(
   [employeeId] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   [lastName] NVARCHAR(20)  NOT NULL,
   [firstName] NVARCHAR(20)  NOT NULL,
   [title] NVARCHAR(30),
   [reportsTo] INTEGER,
   [birthDate] DATETIME,
   [hireDate] DATETIME,
   [address] NVARCHAR(70),
   [city] NVARCHAR(40),
   [state] NVARCHAR(40),
   [country] NVARCHAR(40),
   [postalCode] NVARCHAR(10),
   [phone] NVARCHAR(24),
   [fax] NVARCHAR(24),
   [email] NVARCHAR(60),
   FOREIGN KEY ([reportsTo]) REFERENCES 'employees' ([employeeId])
        ON DELETE NO ACTION ON UPDATE NO ACTION
   )""")
 
    sql_create_index = """CREATE UNIQUE INDEX contact_email
   ON employees (firstName, lastName);"""
 
    conn = create_connection(database) # create a database connection
 
    if conn is not None:    # create table
        create_table(conn, sql_create_table)  # create table
        print("Table successfully created.")
    else:
        print("Error. Cannot create the database connection.")
       
    #inserts the first employee
    conn.execute("INSERT INTO employees (employeeId, lastName, firstName, title, reportsTo, birthDate, hireDate, address, city, state, country, postalCode, phone, fax, email) \
       VALUES (0, 'Cruz', 'Joao', 'CEO', 0, '1999-07-22', '2016-04-01', 'Ruskonlahdenkatu', 'Lappeenranta', 'South Karelia', 'Finland', '53850', '041 136 1841', '1234567', 'joao.cruz@company.fi')");
    
    for i in range(1, 200): #from 1 to 199, since 0 has already been inserted. this totals 200 insertions
        line = string_generator(lastNameList, firstNameList, titleList, addressList, cityList, i)
        #uncomment for debugging if needed
        #print(i)
        #print(line)
        conn.execute(line)
        
    conn.commit()
    print ("Populated successfully.");
   
    #conn.execute("""CREATE INDEX employees_index \
   #ON employees (firstName, lastName);""")
    #print ("Index created successfully.");
   
    #conn.commit()
    conn.close()
   
if __name__ == '__main__':
    main()