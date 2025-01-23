import os
import sqlite3
import random

DBPath = os.path.join(os.path.dirname(__file__), "VolunteerDB.sqlite3") #Defining the pathway to the sqlite3 file

def CreateTables(cursor):

    VolunteersCreation = """
CREATE TABLE IF NOT EXISTS Volunteers(
VolunteerID INTEGER NOT NULL,
Forename VARCHAR(30) NOT NULL,
Surname VARCHAR(30) NOT NULL,
Email VARCHAR(150) NOT NULL,
Password VARCHAR(100) NOT NULL,
MobileNumber INTEGER NOT NULL,
Address VARCHAR(150) NOT NULL,
Postcode VARCHAR(7) NOT NULL,
PRIMARY KEY (VolunteerID));
"""

    EventsCreation = """
CREATE TABLE IF NOT EXISTS Events(
EventID INTEGER NOT NULL,
EventName VARCHAR(50) NOT NULL,
Date DATE NOT NULL,
Time TIME NOT NULL,
Address VARCHAR(150) NOT NULL,
Postcode VARCHAR(7) NOT NULL,
PRIMARY KEY (EventID));
"""

    PrefferedParticipationCreation = """
CREATE TABLE IF NOT EXISTS PreferredParticipation(
ParticipationID INTEGER NOT NULL,
ParticipationName VARCHAR(150) NOT NULL,
ParticipationDescription VARCHAR(300),
PRIMARY KEY (ParticipationID));
"""

    EventAssignmentCreation = """
CREATE TABLE IF NOT EXISTS EventAssignment(
VolunteerID INTEGER NOT NULL,
EventID INTEGER NOT NULL,
FOREIGN KEY (VolunteerID) REFERENCES Volunteers(VolunteerID)
FOREIGN KEY (EventID) REFERENCES Events(EventID)
PRIMARY KEY (VolunteerID, EventID));
"""

    ParticipationAssignment = """
CREATE TABLE IF NOT EXISTS ParticipationAssignment(
VolunteerID INTEGER NOT NULL,
ParticipationID INTEGER NOT NULL,
FOREIGN KEY (VolunteerID) REFERENCES Volunteers(VolunteerID)
FOREIGN KEY (ParticipationID) REFERENCES PreferredParticipation(ParticipationID)
PRIMARY KEY (VolunteerID, ParticipationID));
"""

    cursor.execute(VolunteersCreation) #Executing every command to create all the tables
    cursor.execute(EventsCreation)
    cursor.execute(PrefferedParticipationCreation)
    cursor.execute(EventAssignmentCreation)
    cursor.execute(ParticipationAssignment)


def add_people(n, cursor):

    forenames = ["Sam", "Jack", "James", "Max", "Ben", "Graham", "Hugo", "Anthony", "Zorawar", "Karan", "Archie", "Noah", "George", "Harry", "Ollie", "Toby", "Mark", "Joe", "Caleb", "Ruth", "Charlotte", "Isey", "Issy", "Marco", "Will", "John", "Justin", "Sarah", "Caitlyn", "Owen", "Cole", "Lewis", "Hayden", "Billie", "Lauren", "Alex"]
    surnames = ["Brown", "Davies", "Evans", "Green", "Wilson", "Roberts", "Anderson", "Harrison", "Johnson", "Smith", "Thomas", "Hughes", "Robinson", "Armstrong", "Wright", "Gibson", "Brinkman", "Richell", "Aulakh", "Lock", "Perret", "Toon", "Deighton", "Naumov", "Parry", "Moffat", "Light", "Baker", "Travers", "Ward"]
    letters = list(map(chr, range(ord('A'), ord('Z')+1)))

    for i in range (1, n+1):

            forename = forenames[random.randint(0, len(forenames)-1)]
            surname = surnames[random.randint(0, len(surnames)-1)]
            postcode = f"{letters[random.randint(0, len(letters)-1)]}{letters[random.randint(0, len(letters)-1)]}{random.randint(0, 9)}{random.randint(0, 9)} {random.randint(0, 9)}{letters[random.randint(0, len(letters)-1)]}{letters[random.randint(0, len(letters)-1)]}"
            email = f"{forename[0:4]}{surname}@outlook.com"
            password = f"{surname}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
            mobile_number = int(f"07{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}")

            statement = f"""INSERT INTO Volunteers (VolunteerID, Forename, Surname, Email, Password, MobileNumber, Postcode, Address) 
            VALUES (
            {i}, '{forename}', '{surname}', '{email}', '{password}', {mobile_number}, '{postcode}', 'Gordons School'
            );"""

            cursor.execute(statement)

def add_PP(cursor):

    pp_statement1 = """INSERT INTO PreferredParticipation VALUES (
    1,
    'Restoring Park Benches',
    'Volunteers will fix benches, ensure they are smooth, and apply finishing coats'
    )"""

    pp_statement2 = """INSERT INTO PreferredParticipation VALUES (
    2,
    'Sweeping Leaves',
    'Volunteers will sweep leaves in certain streets and help make the local area look cleaner'
    )"""

    pp_statement3 = """INSERT INTO PreferredParticipation VALUES (
    3,
    'Cleaning Graffiti',
    'Volunteers will scrub illegal graffiti off walls'
    )"""

    cursor.execute(pp_statement1)
    cursor.execute(pp_statement2)
    cursor.execute(pp_statement3)

def AssignPP(cursor):
     
    search_statement = "SELECT VolunteerID FROM Volunteers"
    cursor.execute(search_statement)
    for row in cursor.fetchall():
        PP = random.randint(1, 3)
        statement = f"INSERT INTO ParticipationAssignment VALUES ({row[0]}, {PP})"
        if random.randint(1, 5) == 5 and PP == 2:
            statement2 = f"INSERT INTO ParticipationAssignment VALUES ({row[0]}, {PP-1})"
            cursor.execute(statement2)
            if random.randint(1, 3) == 3:
                statement3 = f"INSERT INTO ParticipationAssignment VALUES ({row[0]}, 3)"
                cursor.execute(statement3)
        if random.randint(1, 5) == 5 and PP == 3:
            statement2 = f"INSERT INTO ParticipationAssignment VALUES ({row[0]}, {random.randint(1, 2)})"
            cursor.execute(statement2)
        cursor.execute(statement)

def add_events(cursor):

    event_statement1 = """INSERT INTO Events VALUES (
    1,
    'Lightwater Village Fete 2022',
    '11/20/2022',
    '10:30',
    'All Saints Church',
    'GU185SJ'
    )"""

    event_statement2 = """INSERT INTO Events VALUES (
    2,
    'Lightwater Village Fete 2023',
    '14/20/2023',
    '10:30',
    'All Saints Church',
    'GU185SJ'
    )"""

    cursor.execute(event_statement1)
    cursor.execute(event_statement2)

def assign_events(cursor):

    search_statement = "SELECT VolunteerID FROM Volunteers"
    cursor.execute(search_statement)
    for row in cursor.fetchall():
        if random.randint(0,3) > 1:
            event = random.randint(1, 2)
            statement = f"INSERT INTO EventAssignment VALUES ({row[0]}, {event})"
            if random.randint(1, 5) > 2 and event == 2:
                statement2 = f"INSERT INTO EventAssignment VALUES ({row[0]}, {event-1})"
                cursor.execute(statement2)
            cursor.execute(statement)

def destroy_db(cursor):
    cursor.execute("DROP TABLE ParticipationAssignment;")
    cursor.execute("DROP TABLE EventAssignment;")
    cursor.execute("DROP TABLE Events;")
    cursor.execute("DROP TABLE Volunteers;")
    cursor.execute("DROP TABLE PreferredParticipation;")

def PopulateDatabase(DBPath):

    SQLiteConnection = sqlite3.connect(DBPath) # Connecting to the sql file
    cursor = SQLiteConnection.cursor() # Creating the cursor

    try:
        destroy_db(cursor)
    except:
        pass

    CreateTables(cursor)

    add_people(10000, cursor)

    add_PP(cursor)

    AssignPP(cursor)

    add_events(cursor)

    assign_events(cursor)

    SQLiteConnection.commit()

    cursor.close()
    SQLiteConnection.close()

PopulateDatabase(DBPath)