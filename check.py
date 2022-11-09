# U6 Coursework
# James Wu

import re

# The syntax for emails - one or more alphanumeric character (+ dots or underscores), an @,
# some number of alphanumeric characters, a . and 2-3 alphanumeric characters
valid = "^[a-z0-9._]+[@][a-z0-9]+[.][a-z0-9]{2,3}$"

# Cannot have consecutive dots / underscores
checkdots = "[._]{2,}"

def validate_email(email):
    flag = bool(re.match(valid, email))
    if re.search(checkdots, email):
        flag = False
    return flag


# uses isbn-13 check digit to check the isbn of books
def check_valid_isbn(isbn):
    if len(isbn) != 13:
        return False
    isbn_split = list(isbn)
    total = 0
    for i in range(0, 12, 2):
        total += int(isbn_split[i])
    for j in range(1,13,2):
        total += 3*int(isbn_split[j])
    needed = 10 - total%10
    if needed == 10:
        needed = 0
    if isbn_split[12] == str(needed):
        return True
    return False


if __name__ == "__main__":
    # Testing some emails
    print(validate_email("a@b.com"), "True")
    print(validate_email("jdifld@diyuwnf.cmc"), "True")
    print(validate_email("jdf_ssfd@r.co"), "True")
    print(validate_email("rdoso@qaa.net"), "True")
    print(validate_email("kdfjls@ww."), "False") # Ends with a dot
    print(validate_email("@djfil.co"), "False") # No characters before @
    print(validate_email("idfosudoiurj"), "False") # No @
    print(validate_email("dfjos@jkdf.sidk"), "False") # 4 characters after dot

    # Testing the dot function
    print(validate_email("asb.cdfj@gmail.com"), "True")
    print(validate_email("asb.c.dfj@gmail.com"), "True")
    print(validate_email("asb..cdfj@gmail.com"), "False") # Two consecutive dots
    print(validate_email("as.b...cdfj@gmail.com"), "False") # Three consecutive dots
    print(validate_email("asb_.cdfj@gmail.com"), "False") # Consecutive _.
    print(validate_email("asb._cdfj@gmail.com"), "False") # Consecutive ._
