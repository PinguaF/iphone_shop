import sqlite3, hashlib, uuid
from flask_login import UserMixin

def register_new_user(first_name, last_name, email, password):
    userid = uuid.uuid4()
    password_hash = generate_password_hash(password)
    with sqlite3.connect("data/user/users.db") as db:
        cursor = db.cursor()
        cursor.execute(f"""SELECT * FROM `main` WHERE `email` == '{email}';""")
        llist = cursor.fetchall()
        print(llist)
        if llist:
            return False
        else:
            cursor = db.cursor()
            cursor.execute(f"""INSERT INTO `main` (`id`, `first_name`, `last_name`, `email`, `password_hash`) 
                           VALUES ('{userid}', '{first_name}', '{last_name}', '{email}', '{password_hash}');""")
            return True

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        with sqlite3.connect("data/user/users.db") as db:
            cursor = db.cursor()
            cursor.execute(f"""SELECT * FROM `main` WHERE `id` == '{id}';""")
            llist = cursor.fetchall()[0]
            self.first_name = llist[1]
            self.last_name = llist[2]
            self.email = llist[3]
            self.password_hash = llist[4]
            self.address = llist[5]
            self.phone = llist[6]

    def check_password(self, password):
        new_hash = generate_password_hash(password)
        if self.password_hash == new_hash:
            return True
        return False

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True  
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
def get_id_from_email(email):
    with sqlite3.connect("data/user/users.db") as db:
        cursor = db.cursor()
        cursor.execute(f"""SELECT `id` FROM `main` WHERE `email` == '{email}';""")
        return cursor.fetchall()[0][0]
    
def generate_password_hash(password):
    h = hashlib.sha256()
    h.update(password.encode('utf-8'))
    password_hash = h.hexdigest()
    return password_hash