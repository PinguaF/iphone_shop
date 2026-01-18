import sqlite3, hashlib
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, userid):
        self.id = userid
        with sqlite3.connect("data\catalog\catalog.db") as db:
            cursor = db.cursor()
            cursor.execute(f"""SELECT * FROM `main` WHERE `id` == {userid};""")
            llist = cursor.fetchall()[0]
            self.first_name = llist[1]
            self.last_name = llist[2]
            self.email = llist[3]
            self.password_hash = llist[4]

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True  
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False