# U6 Coursework
# James Wu

from flask import Flask, render_template, redirect, url_for, request
from database import *
from hash import *
from structures import *
from check import *
from random import shuffle

catalogue = Database()
filters = Filter()
session = Session(catalogue)

app = Flask(__name__)
app.config["SECRET_KEY"] = "eibnskdfs"
app.debug = True

@app.route('/', methods=("GET", "POST"))
def home():
    message = ""

    # Redirect to the relevant homepage
    if session.get_account_logged_in() is not None:
        return redirect(url_for(session.get_account_type()))

    if request.method == "POST":
        form_name = request.form['submit']
        if form_name == "loginform":
            username = request.form.get('username')
            password = request.form.get('password')
            hashpassword = createhash(password)
            cursor = catalogue.login_check(username, hashpassword)
            account = cursor.fetchone()
    
            # If an account exists with these credentials:
            if account:
                session.set_log_in(account[0])
                if password == 'password':
                    return redirect(url_for('changepassword'))
                account_type = session.get_account_type()
                if account_type == "admin":
                    return redirect(url_for('admin'))            
                elif account_type == "teacher":
                    return redirect(url_for('teacher'))
                elif account_type == "student":
                    return redirect(url_for('student'))
            else:
                message = "Username or password incorrect."
                print("No account associated with the entered credentials")

    return render_template("home.html", message=message)

@app.route('/changepassword', methods=("GET", "POST"))
def changepassword():
    message = ""
    account_logged_in = session.get_account_logged_in()
    if account_logged_in != None:
        # If the password of the account is password:
        if catalogue.test_password(account_logged_in, "password"):
            link = "../logout"
            title = "Reset password"
        else:
            link = session.get_redirect_link()
            title = "Change password"
        if request.method == "POST":
            form_name = request.form['submit']
            if form_name == "passform":
                password1 = request.form.get('password1')
                password2 = request.form.get('password2')
                if password1 == password2 and password1.lower() != 'password':
                    message = "Password changed."
                    catalogue.change_password(account_logged_in, password1)
                else:
                    if password1 != password2:
                        message = "Passwords do not match."
                    else:
                        message = "You cannot change the password to 'password'."
        return render_template("changepassword.html", link=link, title=title, message=message)
    else:
        return redirect(url_for("error"))

@app.route('/error')
def error():
    link = session.get_redirect_link()
    return render_template("error.html", link=link)

@app.route('/student')
def student():
    if session.get_account_type() == "student":
        account_logged_in = session.get_account_logged_in()
        person = catalogue.get_person_details(account_logged_in)
        books = catalogue.get_loaned_books(account_logged_in)
        allbooks = catalogue.get_books()
        shuffle(allbooks)
        randombooks = allbooks[0:3]
        for randombook in randombooks:
            randombook.set_department(catalogue.get_subject_name_from_id(randombook.subject))
        return render_template("studenthome.html", person=person, books=books, randombooks=randombooks)
    else:
        return redirect(url_for("error"))

@app.route('/books', methods=("GET", "POST"))
def allbooks():
    books = catalogue.get_filtered_books(filters.sort_by, filters.direction, filters.subject)
    subjects = catalogue.get_subjects()
    for book in books:
        department = catalogue.get_subject_name_from_id(book.subject)
        book.set_department(department)

    if request.method == "POST":
        form_name = request.form['submit']
        if form_name == "filter":
            sort_by = request.form.get('sort_option')
            direction = request.form.get('direction')
            subject = request.form.get('subject')
            filters.apply_filters(sort_by, direction, subject)
            return redirect(url_for("allbooks"))
    return render_template("books.html", books=books, subjects=subjects)

@app.route('/admin', methods=("GET","POST"))
def admin():
    message = ""
    if session.get_account_type() == "admin":
        details = catalogue.get_account_details(session.get_account_logged_in())
        if request.method == "POST":
            form_name = request.form['submit']
            if form_name == "editform":
                username = request.form.get('username')
                forename = request.form.get('forename')
                surname = request.form.get('surname')
                gender = request.form.get('gender')
                dob = request.form.get('dob')
                email = request.form.get('email')
                if email == "" or validate_email(email):
                    catalogue.edit_account(session.get_account_logged_in(), (username, forename, surname, gender, dob, email, ""))
                    return redirect(url_for("admin"))
                else:
                    message = "Invalid email."
        return render_template("adminhome.html", details=details, message=message)
    else:
        return redirect(url_for("error"))

@app.route('/admin/account', methods=("GET", "POST"))
def adminaccount():
    if session.get_account_type() == "admin":        
        message = ""

        accounts = catalogue.get_accounts()
        people = catalogue.get_people_with_fines()
        session.set_account_selected(None)
        if request.method == "POST":
            form_name = request.form['submit']
            if form_name == "accountform":
                username = request.form.get('username')
                forename = request.form.get('forename')
                surname = request.form.get('surname')
                gender = request.form.get('gender')
                dob = request.form.get('dob')
                email = request.form.get('email')
                occupation = request.form.get('occupation')
                if validate_email(email):
                    catalogue.add_account(username, forename, surname, gender, dob, email, occupation)
                    return redirect(url_for("adminaccount"))
                else:
                    message = "Invalid email."
                
            if form_name == "editform":
                accountid = request.form.get('account')
                session.set_account_selected(accountid)
                return redirect(url_for("editaccount"))

            if form_name == "finesform":
                for person in people:
                    if request.form.get(f"fines{person.id}") == "on":
                        catalogue.update_charge(person.id, -(person.charge))
                return redirect(url_for("adminaccount"))

        return render_template("adminaccount.html", accounts=accounts, people=people, message=message)
    else:
        return redirect(url_for("error"))

@app.route('/admin/account/edit', methods=("GET", "POST"))
def editaccount():
    if session.get_account_type() == "admin":
        message = ""
        details = catalogue.get_account_details(session.get_account_selected())
        if request.method == "POST":
            form_name = request.form['submit']
            if form_name == "editform":
                username = request.form.get('username')
                forename = request.form.get('forename')
                surname = request.form.get('surname')
                gender = request.form.get('gender')
                dob = request.form.get('dob')
                email = request.form.get('email')
                occupation = request.form.get('occupation')
                resetpassword = request.form.get('resetpassword')
                if resetpassword == "on":
                    catalogue.change_password(session.get_account_selected(), "password")

                if email == "" or validate_email(email):
                    catalogue.edit_account(session.get_account_selected(), (username, forename, surname, gender, dob, email, occupation))
                    return redirect(url_for("editaccount"))
                else:
                    message = "Invalid email."
        return render_template("admineditaccount.html", details=details, message=message)
    else:
        return redirect(url_for("error"))

@app.route('/admin/account/all', methods=("GET", "POST"))
def adminallaccounts():
    if session.get_account_type() == "admin":
        accounts = catalogue.get_accounts()

        if request.method == "POST":
            form_name = request.form['submit']
            if form_name == "accounts":
                for account in accounts:
                    if request.form.get(f"account{account.pID}") == "on":
                        catalogue.delete_account(account.pID)
                return redirect(url_for("adminallaccounts"))

        return render_template("adminallaccounts.html", accounts = accounts)
    else:
        return redirect(url_for("error"))

@app.route('/admin/book', methods=("GET", "POST"))
def adminbook():
    if session.get_account_type() == "admin":
        message = ""
        
        # For adding functionality
        subjects = catalogue.get_subjects()
        # For missing functionality
        missingbooks = catalogue.get_missing_books()
        missing_statuses = []
        # For create loan functionality
        people = catalogue.get_people()
        books = catalogue.get_books()
        
        if request.method == "POST":
            form_name = request.form['submit']
            if form_name == "bookform":
                title = request.form.get('title')
                author = request.form.get('author')
                isbn = request.form.get('isbn')
                length = request.form.get('length')
                price = request.form.get('price')
                subject = request.form.get('subject')
        
                if check_valid_isbn(isbn):
                    try:
                        catalogue.add_book(title, author, isbn, length, price, subject)
                        message = f"Book {title} added to the database."
                        print(f"Book {title} added to the database.")
                        return redirect(url_for("adminbook"))
                    except:
                        message = "Book not added: an error has occured."

                else:
                    message = "Invalid ISBN."
                    print("ISBN invalid.")
                
            if form_name == "missing":
                for missingbook in missingbooks:
                    missing_statuses.append(request.form.get(f'status{missingbook.libraryid}'))
                catalogue.deal_with_missing_form(missingbooks, missing_statuses)
                return redirect(url_for("adminbook"))

            if form_name == "loan":
                personid = request.form.get('person')
                bookid = request.form.get('book')
                booknumber = request.form.get('booknumber')
                catalogue.assign_book(personid, booknumber, bookid)
                return redirect(url_for("adminbook"))

        return render_template("adminbook.html", subjects=subjects, missingbooks=missingbooks, people=people, books=books, message=message)
    else:
        return redirect(url_for("error"))

@app.route('/admin/book/all', methods=("GET", "POST"))
def adminallbooks():
    if session.get_account_type() == "admin":
        books = catalogue.get_books()
        if request.method == "POST":
            form_name = request.form['submit']
            if form_name == "books":
                for book in books:
                    if request.form.get(f"book{book.id}") == "on":
                        catalogue.delete_book(book.id)
                return redirect(url_for('adminallbooks'))
        return render_template("adminallbooks.html", books = books)
    else:
        return redirect(url_for("error"))

@app.route('/admin/class', methods=("GET", "POST"))
def adminclass():
    if session.get_account_type() == "admin":
        session.set_class_selected(None)
        people = catalogue.get_accounts()
        classes = catalogue.get_classes()
        subjects = catalogue.get_subjects()

        if request.method == 'POST':
            form_name = request.form['submit']

            if form_name == "classform":
                person = request.form.get('person')
                theclass = request.form.get('theclass')
                catalogue.add_personclass(person, theclass)
                return redirect(url_for('adminclass'))

            if form_name == "moveform":
                class1 = request.form.get('firstclass')
                class2 = request.form.get('secondclass')
                catalogue.move_class(class1, class2)
                return redirect(url_for('adminclass'))

            if form_name == "removeform":
                theclass = request.form.get('theclass')
                return redirect(("/admin/class/{}").format(theclass))

            if form_name == "createform":
                classname = request.form.get('classname')
                subject = request.form.get('subject')
                catalogue.create_class(subject, classname)
                return redirect(url_for('adminclass'))

            if form_name == "renameform":
                theclass = request.form.get('selectclass')
                newname = request.form.get('newname')
                catalogue.rename_class(theclass, newname)
                return redirect(url_for('adminclass'))

        return render_template("adminclass.html", people = people, classes = classes, firstclass = classes, secondclass = classes, subjects = subjects)
    else:
        return redirect(url_for("error"))

@app.route('/admin/class/<id>', methods=("GET", "POST"))
def classstudents(id):
    if session.get_account_type() == "admin":
        session.set_class_selected(id)
        students = catalogue.get_students(id)
        if request.method == "POST":
            form_name = request.form['submit']
            if form_name == "remove":
                for student in students:
                    if request.form.get(f"remove{student.id}") == "on":
                        catalogue.remove_student(student.id, id)
                return redirect(f"/admin/class/{id}")
        return render_template("classstudents.html", students = students)
    else:
        return redirect(url_for("error"))

@app.route('/teacher')
def teacher():
    if session.get_account_type() == "teacher":
        session.set_class_selected(None)
        teacherobject = catalogue.get_person_details(session.get_account_logged_in())
        classes = catalogue.get_teacher_classes(session.get_account_logged_in())
        return render_template("teacher.html", classes=classes, teacherobject=teacherobject)
    else:
        return redirect(url_for("error"))

@app.route('/teacher/<id>', methods=("GET", "POST"))
def teacherclass(id):
    if session.get_account_type() == "teacher":
        session.set_class_selected(id)
        
        classobject = catalogue.get_class_details(id)
        classes = catalogue.get_teacher_classes(session.get_account_logged_in())
        otherclasses = []
        for element in classes:
            # If the ID of the AClass object isn't the selected class ID then add it to otherclasses
            if int(element.cID) != int(id):
                otherclasses.append(element)

        # For assign part
        students = catalogue.get_students(id)
        books = catalogue.get_books()
        # For return part
        loanedbooks = catalogue.get_loaned_books_of_a_class(id)

        if request.method == "POST":
            form_name = request.form['submit']
            if form_name == "assign":
                bookid = request.form.get('book')
                booknumbers = []
                for student in students:
                    booknumbers.append(request.form.get('booknumber{}'.format(student.id)))
                catalogue.assign_books(students, booknumbers, bookid)
                return redirect(f'/teacher/{id}')
        return render_template("teacherclass.html", students=students, books=books, loanedbooks=loanedbooks, otherclasses=otherclasses, classobject=classobject)
    else:
        return redirect(url_for("error"))

@app.route('/teacher/return/<bookid>', methods=("GET", "POST"))
def teacherclassreturn(bookid):
    if session.get_account_type() == "teacher":
        class_selected = session.get_class_selected()
        students = catalogue.get_students_borrowing_a_book(class_selected, bookid)
        if request.method == "POST":
            form_name = request.form['submit']
            if form_name == "update":
                statuses = []
                for student in students:
                    statuses.append(request.form.get(f'status{student.id}'))
                catalogue.update_statuses(students, statuses, bookid)
                return redirect(f'/teacher/return/{bookid}')
        return render_template("teacherreturn.html", students = students, classselected=class_selected)
    else:
        return redirect(url_for("error"))

@app.route('/logout')
def logout():
    session.set_log_in(None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()