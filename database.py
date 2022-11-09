# U6 Coursework
# James Wu

import sqlite3
import csv
from datetime import date
from hash import *
from structures import *

class Database:
    def __init__(self):
        """Initialises the class"""
        self.__conn = sqlite3.connect("cat.db", check_same_thread=False)
        print("Database opened successfully")

    def show_output(self, cursor):
        """
        Displays each row of a cursor
        Takes a cursor as a parameter
        """
        for row in cursor:
            print(row)

    def close(self):
        """Closes the database"""
        self.__conn.close()

    def display_table(self, table):
        """Displays the contents of a table in the database.
        Takes a string as a parameter"""
        query = """SELECT * FROM {}""".format(table)
        cur = self.__conn.execute(query)
        self.show_output(cur)

    def create_tables(self):

        """Creates the tables needed for the database"""

        subject_command = """CREATE TABLE IF NOT EXISTS Subject(
            SubjectID INTEGER PRIMARY KEY,
            SubjectName TEXT NOT NULL
        );
        """
        self.__conn.execute(subject_command)
        print("Subject table created successfully.")

        book_command = """CREATE TABLE IF NOT EXISTS Book(
            BookID INTEGER PRIMARY KEY,
            Title text NOT NULL,
            Author TEXT NOT NULL,
            ISBN TEXT NOT NULL UNIQUE,
            Length INTEGER NOT NULL,
            Price REAL NOT NULL,
            SubjectID INTEGER NOT NULL,
            FOREIGN KEY(SubjectID) REFERENCES Subject(SubjectID)
        );
        """
        self.__conn.execute(book_command)
        print("Book table created successfully.")

        person_command = """CREATE TABLE IF NOT EXISTS Person(
            PersonID INTEGER NOT NULL,
            Forename TEXT,
            Surname TEXT,
            Gender TEXT,
            DateOfBirth TEXT,
            Email TEXT UNIQUE,
            Occupation TEXT,
            Charge REAL
        );
        """
        self.__conn.execute(person_command)
        print("Person table created successfully.")

        loan_command = """CREATE TABLE IF NOT EXISTS Loan(
            LoanID INTEGER PRIMARY KEY,
            PersonID INTEGER NOT NULL,
            LibraryID INTEGER NOT NULL,
            DateStarted TEXT NOT NULL,
            FOREIGN KEY(PersonID) REFERENCES Person(PersonID),
            FOREIGN KEY(LibraryID) REFERENCES Library(LibraryID)
        );
        """
        self.__conn.execute(loan_command)
        print("Loan table created successfully.")

        account_command = """CREATE TABLE IF NOT EXISTS Account(
            PersonID INTEGER PRIMARY KEY,
            Username TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            FOREIGN KEY(PersonID) REFERENCES Person(PersonID)
        );
        """
        self.__conn.execute(account_command)
        print("Account table created successfully.")

        library_command = """CREATE TABLE IF NOT EXISTS Library(
            LibraryID INTEGER PRIMARY KEY,
            BookID INTEGER,
            Availability TEXT,
            Condition TEXT,
            BookNumber TEXT,
            FOREIGN KEY(BookID) REFERENCES Book(BookID)
        );
        """
        self.__conn.execute(library_command)
        print("Library table created successfully.")

        class_command = """CREATE TABLE IF NOT EXISTS Class(
            ClassID INTEGER PRIMARY KEY,
            SubjectID INTEGER NOT NULL,
            ClassName TEXT NOT NULL,
            FOREIGN KEY(SubjectID) REFERENCES Subject(SubjectID)
        );
        """
        self.__conn.execute(class_command)
        print("Class table created successfully")

        personclass_command = """CREATE TABLE IF NOT EXISTS PersonClass(
            PersonID INTEGER NOT NULL,
            ClassID INTEGER NOT NULL,
            FOREIGN KEY(PersonID) REFERENCES Person(PersonID)
            FOREIGN KEY(ClassID) REFERENCES Class(ClassID)
        );
        """
        self.__conn.execute(personclass_command)
        print("PersonClass table created successfully.")

    def insert_mock_data(self, table):

        """Inserts mock data into the table, taking table (a string) as a parameter"""

        with open("static/csv/{0}.csv".format(table), encoding="utf8") as csvfile:
            location_reader = csv.DictReader(csvfile)
            for row in location_reader:

                if table == "subject":
                    query = f"""INSERT INTO Subject(SubjectID, SubjectName) VALUES ({row['SubjectID']}, "{row['SubjectName']}");"""
                elif table == "book":
                    query = f"""INSERT INTO Book(BookID, Title, Author, ISBN, Length, Price, SubjectID) VALUES ({row['BookID']}, 
                                "{row['Title']}", "{row['Author']}", "{row['ISBN']}", {row['Length']}, "{row['Price']}", {row['SubjectID']});"""
                elif table == "person":
                    query = f"""INSERT INTO Person(PersonID, Forename, Surname, Gender, DateOfBirth, Email, Occupation, Charge) 
                                VALUES ({row['PersonID']}, "{row['Forename']}", "{row['Surname']}", "{row['Gender']}", "{row['DateOfBirth']}", 
                                "{row['Email']}", "{row['Occupation']}", {row['Charge']});"""
                elif table == "loan":
                    query = f"""INSERT INTO Loan(LoanID, PersonID, LibraryID, DateStarted) 
                                VALUES ({row['LoanID']}, {row['PersonID']},{row['LibraryID']}, "{row['DateStarted']}");"""
                elif table == "account":
                    hashed_password = createhash(row['Password'])
                    query = """INSERT INTO Account(PersonID, Username, Password) VALUES ({}, "{}", "{}");""".format(row['PersonID'], row['Username'], hashed_password)
                elif table == "library":
                    query = f"""INSERT INTO Library(LibraryID, BookID, Availability, Condition, BookNumber) 
                                VALUES ({row['LibraryID']}, {row['BookID']}, "{row['Availability']}", "{row['Condition']}", "{row['BookNumber']}");"""
                elif table == "class":
                    query = f"""INSERT INTO Class(ClassID, SubjectID, ClassName) VALUES ({row['ClassID']}, {row['SubjectID']}, "{row['ClassName']}");"""
                elif table == "personclass":
                    query = f"""INSERT INTO PersonClass(PersonID, ClassID) VALUES ({row['PersonID']}, {row['ClassID']});"""

                try:
                    self.__conn.execute(query)
                    self.__conn.commit()
                    print("Inserted into {}".format(table))
                except:
                    print("Failed to insert into {}.".format(table))
                    print(query)

    def populate_mock_data(self):

        """Populates the whole database with mock data"""

        self.insert_mock_data("subject")
        self.insert_mock_data("book")
        self.insert_mock_data("person")
        self.insert_mock_data("loan")
        self.insert_mock_data("account")
        self.insert_mock_data("library")
        self.insert_mock_data("class")
        self.insert_mock_data("personclass")

    def login_check(self, username, password):

        """Returns the cursor object containing accounts with the username and password passed as parameters"""

        query = """SELECT * FROM Account WHERE Username = "{0}" AND Password = "{1}";""".format(username, password)
        cursor = self.__conn.execute(query)
        return cursor

    def get_subjects(self):
        """Returns a list of all the Subject objects in the database"""
        query = """SELECT * FROM Subject"""
        cur = self.__conn.execute(query)
        subjects = []
        for element in cur:
            subjects.append(Subject(element))
        return subjects

    def create_ID(self, table):
        """Creates a new ID for adding a new record, taking table (a string) as a parameter"""
        idname = table + "ID"
        query = """SELECT MAX({}) FROM {}""".format(idname, table)
        cur = self.__conn.execute(query)
        for row in cur:
            value = row
        try:
            value = value[0]
            ID = int(value) + 1
        except:
            ID = 1
        return ID

    def add_book(self, title, author, isbn, length, price, subjectid):
        """Adds a book to the book table, taking the above parameters (strings except for subjectid and length, which are integers)"""
        bookid = self.create_ID("Book")
        query = """INSERT INTO Book VALUES({}, "{}", "{}", "{}", {}, "{}", {})""".format(bookid, title, author, isbn, length, price, subjectid)
        self.__conn.execute(query)
        self.__conn.commit()
        print(title, "successfully added to database")

    def get_books(self):
        """Returns a list of all the books stored in the database as Book objects"""
        query = """SELECT * FROM Book"""
        cur = self.__conn.execute(query)
        books = []
        for element in cur:
            books.append(Book(element))
        return books

    def delete_book(self, id):
        """Removes a book and its associated loans from the database, taking the BookID (integer) as a parameter"""
        # remove the book from the book table
        query = """DELETE FROM Book WHERE BookID = {}""".format(id)
        self.__conn.execute(query)
        
        # remove all associated loans with the book
        for libraryid in self.get_libraryid_from_bookid(id):
            query2 = f"""DELETE FROM Loan WHERE LibraryID = {libraryid}"""
            self.__conn.execute(query2)
            self.__conn.commit()
            print("Loan deleted.")

    def add_account(self, username, forename, surname, gender, dob, email, occupation):
        """Adds an account to the database by adding a Person and Account record, taking the above parameters"""
        personid = self.create_ID("Person")
        # Add a record into the person table
        query = """INSERT INTO Person VALUES({}, "{}", "{}", "{}", "{}", "{}", "{}", 0.00)""".format(personid, forename, surname, gender, dob, email, occupation)
        self.__conn.execute(query)

        # Add a record into the account table
        # Store the hashed version of 'password' as the first password, able to be changed upon first login
        password = createhash("password")
        query2 = """INSERT INTO Account VALUES({}, "{}", "{}")""".format(personid, username, password)
        self.__conn.execute(query2)
        self.__conn.commit()
        print(forename, surname, "successfully added to database")

    def get_accounts(self):
        """Returns all the accounts stored in the database as a list of Account objects"""
        accounts = []
        query = """SELECT * FROM Person, Account WHERE Person.PersonID = Account.PersonID ORDER BY Person.Surname ASC"""
        cur = self.__conn.execute(query)
        for element in cur:
            accounts.append(Account(element))
        return accounts

    def delete_account(self, id):
        """Removes an account and their loans from the database, taking PersonID (integer) as a paramter"""
        # remove the account from the person and account table
        query = """DELETE FROM Person WHERE PersonID = {}""".format(id)
        query2 = """DELETE FROM Account WHERE PersonID = {}""".format(id)
        query3 = """DELETE FROM Loan WHERE PersonID = {}""".format(id)
        self.__conn.execute(query)
        self.__conn.execute(query2)
        self.__conn.execute(query3)
        self.__conn.commit()

    def change_password(self, id, password):
        """Changes the password of an account, taking the password (string) and PersonID (integer) as parameters"""
        hashedpassword = createhash(password)
        query = """UPDATE Account SET password = "{}" WHERE PersonID = {}""".format(hashedpassword, id)
        self.__conn.execute(query)
        self.__conn.commit()

        print("Password successfully changed")

    def get_classes(self):
        """Returns all the classes stored in the database as a list of AClass objects"""
        classes = []
        cur = self.__conn.execute("""SELECT * FROM Class""")
        for element in cur:
            classes.append(AClass(element))
        return classes

    def add_personclass(self, personid, classid):
        """Adds a person to a class, taking PersonID and ClassID (both integers) as parameters"""
        self.__conn.execute(("""INSERT INTO PersonClass VALUES({}, {})""").format(personid, classid))
        self.__conn.commit()
        print(("Person with id {} successfully added to class with id {}.").format(personid, classid))

    def move_class(self, class1id, class2id):
        """Moves all the people in a class to another, taking two ClassIDs as paramters"""
        self.__conn.execute(("""UPDATE PersonClass SET ClassID = {} WHERE ClassID = {}""").format(class2id, class1id))
        self.__conn.commit()
        print(("Moved everyone in Class {} to Class {}").format(class1id, class2id))

    def get_students(self, classid):
        """Returns all the students in a specific class stored in the database as a list of type ClassStudent"""
        students = []

        query = ("""SELECT Person.PersonID, Person.Forename, Person.Surname
            FROM Person, PersonClass
            WHERE PersonClass.ClassId = {}
            AND Person.PersonID = PersonClass.PersonID
            AND Person.Occupation = 'student'
            ORDER BY Person.Surname ASC
        """).format(classid)

        cur = self.__conn.execute(query)
        for element in cur:
            students.append(ClassStudent(element))
        return students

    def remove_student(self, personid, classid):
        """Removes a student from a class, taking PersonID and ClassID (both integers) as parameters"""
        query = ("""DELETE FROM PersonClass WHERE PersonID = {} AND ClassId = {}""").format(personid, classid)
        print(f"Student with id {personid} removed from the class.")
        self.__conn.execute(query)
        self.__conn.commit()

    def create_class(self, subjectid, name):
        """Creates a new class, taking SubjectID (integer) and a name (string) as paramters"""
        id = self.create_ID("Class")
        self.__conn.execute(("""INSERT INTO Class VALUES({}, {}, '{}')""").format(id, subjectid, name))
        self.__conn.commit()

    def rename_class(self, classid, newname):
        """Renames a class, taking the new name (string) and the ClassID (integer) as parameters"""
        self.__conn.execute(f"UPDATE Class SET ClassName = '{newname}' WHERE ClassID = {classid}")
        self.__conn.commit()

    def get_teacher_classes(self, personid):
        """Returns all the classes that the teacher teaches as a list of AClass objects"""
        classes = []
        query = """SELECT Class.ClassID, Class.SubjectID, Class.Classname
            FROM Person, PersonClass, Class
            WHERE Person.Occupation == 'teacher'
            AND Person.PersonID == PersonClass.PersonID
            AND Person.PersonID == {}
            AND PersonClass.ClassID == Class.ClassID
        """.format(personid)

        cur = self.__conn.execute(query)
        for element in cur:
            classes.append(AClass(element))
        return classes

    def get_class_details(self, classid):
        """Returns the AClass Object associated with the ClassID (integer) which is taken as a parameter"""
        cur = self.__conn.execute(f"SELECT * FROM Class WHERE ClassID = {classid}")
        for element in cur:
            return AClass(element)
        return None

    def get_availability(self, libraryid):
        """Returns the availability (string) of a book with the LibraryID (integer) passed as a parameter"""
        query = f"""SELECT Availability FROM Library WHERE LibraryID = {libraryid}"""
        cur = self.__conn.execute(query)
        for element in cur:
            return element[0]

    def set_availability(self, libraryid, status):
        """Sets the availability of a book of the LibraryID (integer) to the status (string)"""
        query = f"""UPDATE Library SET Availability = '{status}' WHERE LibraryID = {libraryid}"""
        self.__conn.execute(query)
        self.__conn.commit()

    def get_bookid_from_libraryid(self, libraryid):
        """Returns the BookID, taking the LibraryID (integer) as the parameter"""
        query = f"""SELECT BookID FROM Library WHERE LibraryID = {libraryid}"""
        cur = self.__conn.execute(query)
        for element in cur:
            return element[0]

    def get_libraryid_from_bookid(self, bookid):
        """Returns a list of LibraryIDs which each have the same BookID (integer) passed as the parameter"""
        ids = []
        query = f"""SELECT LibraryID FROM Library WHERE BookID = {bookid}"""
        cur = self.__conn.execute(query)
        for element in cur:
            ids.append(element[0])
        return ids

    def get_student_textbook(self, studentid, libraryid):
        """Returns a boolean, depending on if the student already has a book of the same type.
        Takes StudentID and LibraryID as parameters (both integers)"""
        bookid = self.get_bookid_from_libraryid(libraryid)
        query = f"""SELECT BookID FROM Loan, Library WHERE PersonId = {studentid} AND Loan.LibraryID = Library.LibraryID"""
        cur = self.__conn.execute(query)
        for record in cur:
            if record[0] == bookid:
                print("Student already has the textbook")
                return True
        return False

    def create_loan(self, personid, libraryid):
        """Creates a loan, taking the PersonID and LibraryID as parameters (both integers)"""
        if self.get_availability(libraryid) == "Available" and not self.get_student_textbook(personid, libraryid):
            loanid = self.create_ID("Loan")
            datestarted = date.today()
            query = """INSERT INTO Loan Values({}, {}, {}, '{}')""".format(loanid, personid, libraryid, datestarted)
            self.__conn.execute(query)
            print(f"New loan created with person {personid}, libraryid {libraryid}, date {datestarted}.")
            self.__conn.commit()
            self.set_availability(libraryid, 'Loaned')
        else:
            print(f"Loan not created.")

    def create_library_book(self, bookid, booknumber):
        """Creates a new Library record with the BookID (integer) and Booknumber (string) as parameters"""
        libraryid = self.create_ID("Library")
        query = f"""INSERT INTO Library Values({libraryid}, {bookid}, 'Available', 'Good', '{booknumber}')"""
        self.__conn.execute(query)
        print(f"New library record created with book id {bookid} and booknumber {booknumber}")
        self.__conn.commit()
        return libraryid

    def get_library_id(self, bookid, booknumber):
        """Returns the LibraryID (integer) of the book with the same BookID (integer) and Booknumber (string), but returns NoneType if no book exists"""
        query = f"""SELECT * FROM Library WHERE Booknumber = '{booknumber}' AND BookID = {bookid}"""
        cur = self.__conn.execute(query)
        for libraryid in cur:
            if libraryid is not None:
                return libraryid[0]
            else:
                return None

    def assign_book(self, studentid, bookid, booknumber):
        """Assigns a book to a student by creating a loan (and a new library book if necessary)
        Takes StudentID, BookID (integers) and Booknumber (string) as parameters"""
        libraryid = self.get_library_id(bookid, booknumber)
        if libraryid is None:
            libraryid = self.create_library_book(bookid, booknumber)
        self.create_loan(studentid, libraryid)
    
    def assign_books(self, students, booknumbers, bookid):
        """Assigns a set of books to a set of students, taking lists Students and Booknumbers and integer BookID as parameters"""
        for i in range(len(students)):
            if booknumbers[i] != "":
                self.assign_book(students[i].id, bookid, booknumbers[i])

    def get_loaned_books_of_a_class(self, classid):
        """Returns all the books that have been loaned to students in the class, returns a list of book objects.
        Takes ClassID (integer) as parameter."""
        
        studentids = []
        bookids = []
        books = []

        students = self.get_students(classid)
        for student in students:
            studentids.append(student.id)
       
        for studentid in studentids:
            query = f"""SELECT BookId
                FROM Library, Loan
                WHERE Loan.PersonID = {studentid}
                AND Loan.LibraryID = Library.LibraryID
            """
            cur = self.__conn.execute(query)
            for element in cur:
                bookid = element[0]
                if bookid not in bookids:
                    bookids.append(bookid)
        
        for id in bookids:
            query = f"""SELECT * FROM Book WHERE BookID = {id}"""
            cur = self.__conn.execute(query)
            for element in cur:
                books.append(Book(element))

        return books

    def get_students_borrowing_a_book(self, classid, bookid):
        """Returns a list of students borrowing a certain book in a certain class, taking ClassID and BookID as parameters (integers)"""
        
        # A list of all the library records with the book id
        libraryids = self.get_libraryid_from_bookid(bookid)
        # A list of ClassPerson objects, representing the students in the class
        students = self.get_students(classid)
        
        neededstudents = []

        """query1 = f"SELECT LibraryID FROM Library WHERE BookId = {bookid}"
        cur = self.__conn.execute(query1)
        for element in cur:
            libraryids.append(element[0])"""
        
        for student in students:
            query = f"""SELECT Library.LibraryID, Booknumber
                FROM Library, Loan
                WHERE PersonID = {student.id}
                AND Library.LibraryID = Loan.LibraryID"""
            cur = list(self.__conn.execute(query))
            for book in cur:
                if book[0] in libraryids:
                    student.set_book_number(book[1])
                    neededstudents.append(student)
        
        return neededstudents
        
    def get_person_name_from_id(self, personid):
        """Returns a string of the person's forename and surname by their id (integer) passed as an argument"""
        return " ".join(list(self.__conn.execute(f"SELECT Forename, Surname FROM Person WHERE PersonID = {personid}"))[0])

    def get_missing_books(self):
        """Returns a list of Book objects of all the missing books in the database"""
        books = []
        query = """SELECT Book.BookID, Title, Author, ISBN, Length, Price, SubjectID, LibraryID
            FROM Library, Book
            WHERE Availability = 'Missing' AND Library.BookID = Book.BookID"""
        cur = self.__conn.execute(query)
        for element in cur:
            bookitems = element[0:7] # The first 7 items are the attributes of the book
            currentbook = Book(bookitems)
            libraryid = element[7] # The eighth item is the library id
            currentbook.set_library_id(libraryid) # Set the libraryid of the book object created
            cur2 = list(self.__conn.execute(f"SELECT PersonID FROM Loan WHERE LibraryID = {libraryid}")) # Find the person borrowing the book with the libraryid
            studentid = cur2[0][0]
            currentbook.set_student_id(studentid) # Set the studentid of the book object created
            studentname = self.get_person_name_from_id(studentid) # Get the name of the student borrowing the book
            currentbook.set_student_borrowing(studentname) # Change the book instance attribute to the name of the student
            books.append(currentbook)
        return books

    def get_libraryid_from_bookid_and_booknumber(self, bookid, booknumber):
        """Returns the LibraryID from the BookID and Booknumber (both integers) passed as arguments"""
        query = f"""SELECT LibraryID FROM Library WHERE BookID = {bookid} AND Booknumber = '{booknumber}'"""
        cur = self.__conn.execute(query)
        for element in cur:
            return element[0]
        return None

    def remove_loan(self, loanid):
        """Deletes a loan record from the database, taking LoanID (integer) as parameter"""
        query = f"""DELETE FROM Loan WHERE LoanID = {loanid}"""
        self.__conn.execute(query)
        self.__conn.commit()

    def get_loan_id(self, studentid, libraryid):
        """REturns the LoanID from the IDs passed as parameter, if none exists NoneType is returned."""
        query = f"""SELECT LoanID FROM Loan WHERE PersonID = {studentid} AND LibraryID = {libraryid}"""
        cur = self.__conn.execute(query)
        for element in cur:
            return element[0]
        return None

    def update_statuses(self, students, statuses, bookid):
        """Updates the statuses of all the students' loaned books, taking lists students, statuses and integer BookID as parameters"""
        if len(students) != len(statuses):
            print("Student list and status list inconsistent")
            return None

        for i in range(len(students)):
            if statuses[i] != "Loaned":
                libraryid = self.get_libraryid_from_bookid_and_booknumber(bookid, students[i].booknumber)
                self.set_availability(libraryid, statuses[i])
                if statuses[i] == "Available":
                    loanid = self.get_loan_id(students[i].id, libraryid)
                    self.remove_loan(loanid)
                    print(students[i].forename, students[i].surname + "'s loan removed from the database.")

    def get_charge(self, personid):
        """Returns the charge of a person of PersonID (integer) passed as argument."""
        cur = self.__conn.execute(f"SELECT Charge FROM Person WHERE PersonID = {personid}")
        for element in cur:
            return element[0]

    def update_charge(self, personid, amount):
        """Updates the charge of a person having the PersonID (integer) passed as parameter, changing the amount by Amount (float)"""
        currentcharge = self.get_charge(personid)
        newcharge = currentcharge+amount
        if newcharge < 0:
            newcharge = 0   # So that the system cannot owe a person any money
        self.__conn.execute(f"UPDATE Person SET Charge = {newcharge} WHERE PersonID = {personid}")
        personname = self.get_person_name_from_id(personid)
        print(f"{personname}'s charge updated to {newcharge}")
        self.__conn.commit()

    def remove_library_book(self, libraryid):
        """Deletes the library book of LibraryID (integer) passed as argument"""
        self.__conn.execute(f"DELETE FROM Library WHERE LibraryID = {libraryid}")
        print(f"{libraryid} deleted from the database.")
        self.__conn.commit()

    def deal_with_missing_form(self, books, values):
        """Takes lists of Book objects and the new statuses (list of strings) and processes the submitted missing form"""
        if len(books) != len(values):
            print("Invalid arguments.")
            return
        
        for i in range(len(books)):
            currentlibraryid = books[i].libraryid
            currentstudentid = books[i].studentid
            currentloanid = self.get_loan_id(currentstudentid, currentlibraryid)
            if values[i] == "Returned":
                self.set_availability(currentlibraryid, "Available")
                self.remove_loan(currentloanid)
            elif values[i] == "Replaced":
                self.remove_library_book(currentlibraryid)
                price = books[i].price
                self.update_charge(currentstudentid, price)
                self.remove_loan(currentloanid)
    
    def get_people_with_fines(self):
        """Returns a list of type Person of all those who have a fine"""
        people = []
        cur = self.__conn.execute("""SELECT * FROM Person WHERE Charge > 0 ORDER BY Surname ASC""")
        for element in cur:
            people.append(Person(element))
        return people

    def get_person_details(self, id):
        """Returns the Person object associated with the ID taken as parameter"""
        cur = self.__conn.execute(f"SELECT * FROM Person WHERE PersonID = {id}")
        for element in cur:
            return Person(element)
        return None

    def get_account_details(self, id):
        """Returns the Account object associated with the ID taken as parameter"""
        cur = self.__conn.execute(f"SELECT * FROM Person, Account WHERE Person.PersonID = Account.PersonID AND Person.PersonID = {id}")
        for element in cur:
            return Account(element)
        return None

    def get_loaned_books(self, personid):
        """Returns a list of Book objects that the person with the PersonID taken as parameter has borrowed"""
        books = []
        query = f"""SELECT BookID FROM Loan, Library WHERE PersonID = {personid} AND Loan.LibraryID = Library.LibraryID"""
        cur = self.__conn.execute(query)
        for element in cur:
            cur2 = list(self.__conn.execute(f"""SELECT * FROM Book WHERE BookID = {element[0]}"""))
            for item in cur2:
                books.append(Book(item))
        return books

    def get_subject_name_from_id(self, subjectid):
        """Returns the name of a subject based on the SubjectID passed as parameter"""
        cur = self.__conn.execute(f"""SELECT SubjectName FROM Subject WHERE SubjectID = {subjectid}""")
        for element in cur:
            return element[0]
        return None

    def get_filtered_books(self, sort_by="BookID", direction="ASC", subject="None"):
        """Returns a list of Book objects, ordered by the filters passed as parameters (strings)"""
        books = []
        parameter = ""
        if subject != "None":
            parameter = f"WHERE SubjectID = {subject}"
        query = f"""SELECT * FROM Book {parameter} ORDER BY {sort_by} {direction}"""
        print(query)
        cur = self.__conn.execute(query)
        for book in cur:
            books.append(Book(book))
        return books
    
    def get_people(self):
        """Returns a list of Person objects of everybody stored in the database"""
        people = []
        cur = self.__conn.execute("SELECT * FROM Person ORDER BY Surname ASC")
        for element in cur:
            people.append(Person(element))
        return people

    def get_occupation(self, personid):
        """Returns the occupation of a person with the PersonID (integer) passed as the parameter"""
        cur = self.__conn.execute(f"SELECT Occupation FROM Person WHERE PersonID = {personid}")
        for element in cur:
            return element[0]
        return None

    def test_password(self, personid, test):
        """Returns a boolean by testing a password against the personid's."""
        cur = self.__conn.execute(f"SELECT Password FROM Account WHERE PersonID = {personid}")
        for element in cur:
            hashedpass = element[0]
        testpass = createhash(test)
        if hashedpass == testpass:
            return True
        else:
            return False

    def update_person_detail(self, personid, detailfield, newdetail, table):
        """Updates a field of a person's information, taking the PersonID (integer), detailfield, newdetail and table (strings) as parameters"""
        if newdetail != "":
            query = f"""UPDATE {table} SET {detailfield} = '{newdetail}' WHERE PersonID = {personid}"""
            print(query)
            self.__conn.execute(query)
            self.__conn.commit()

    def edit_account(self, personid, newinfo):
        """Edits the profile of PersonID (integer) with the new information (list of strings) taken in as parameters"""
        info_order = ("Username", "Forename", "Surname", "Gender", "DateOfBirth", "Email", "Occupation")
        for i in range(len(info_order)):
            if i == 0:
                self.update_person_detail(personid, info_order[i], newinfo[i], "Account")
            else:
                self.update_person_detail(personid, info_order[i], newinfo[i], "Person")


def main():
    catalogue = Database()
    catalogue.create_tables()
    catalogue.populate_mock_data()
    catalogue.close()

if __name__ == "__main__":
    main()