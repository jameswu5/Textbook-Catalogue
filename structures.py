# U6 Coursework
# James Wu

class Subject:
    def __init__(self, tuple):
        self.id, self.name = tuple

class Book:
    def __init__(self, tuple):
        self.id, self.title, self.author, self.isbn, self.length, self.price, self.subject = tuple
        self.studentborrowing = None
        self.studentid = None
        self.libraryid = None
        self.department = None

    def set_student_borrowing(self, studentid):
        self.studentborrowing = studentid

    def set_student_id(self, studentid):
        self.studentid = studentid

    def set_library_id(self, libraryid):
        self.libraryid = libraryid

    def set_department(self, subjectname):
        self.department = subjectname

class Account:
    def __init__(self, tuple):
        self.pID, self.forename, self.surname, self.gender, self.dob, self.email, self.occupation, self.charge, self.aID, self.username, self.password = tuple
    
class AClass:
    def __init__(self, tuple):
        self.cID, self.sID, self.name = tuple

class ClassStudent:
    def __init__(self, tuple):
        self.id, self.forename, self.surname = tuple
        self.booknumber = None
    
    def set_book_number(self, booknumber):
        self.booknumber = booknumber

class Person:
    def __init__(self, tuple):
        self.id, self.forename, self.surname, self.gender, self.dob, self.email, self.occupation, self.charge = tuple

class Filter:
    def __init__(self):
        self.sort_by = "BookID"
        self.direction = "ASC"
        self.subject = "None"

    def apply_filters(self, sort, direction, subject):
        self.sort_by = sort
        self.direction = direction
        self.subject = subject

class Session:
    def __init__(self, database):
        self.__database = database
        self.set_log_in(None)
        self.__class_selected = None
        self.__account_selected = None
        
    def set_log_in(self, accountid):
        self.__account_logged_in = accountid
        if accountid is not None:
            self.__account_type = self.__database.get_occupation(accountid)
        else:
            self.__account_type = None
        
    def set_class_selected(self, classid):
        self.__class_selected = classid

    def set_account_selected(self, accountid):
        self.__account_selected = accountid

    def get_account_logged_in(self):
        return self.__account_logged_in

    def get_account_type(self):
        return self.__account_type

    def get_class_selected(self):
        return self.__class_selected

    def get_account_selected(self):
        return self.__account_selected

    def reset(self):
        self.__account_logged_in = None
        self.__account_type = None
        self.__class_selected = None
        self.__account_selected = None

    def get_redirect_link(self):
        if self.__account_type == "student":
            return "/student"
        elif self.__account_type == "teacher":
            return "/teacher"
        elif self.__account_type == "admin":
            return "/admin"
        else:
            return "../"