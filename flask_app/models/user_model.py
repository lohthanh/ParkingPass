from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
import re
from flask import flash
from flask_app.models import keycard_model



ALPHA = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
ALPHANUMERIC = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
)


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.user_level = data["user_level"]
        self.employee_id = data["employee_id"]
        self.password = data["password"]
        self.last_logged_on = data["last_logged_on"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.keycards = []
        

    @classmethod
    def create(cls, data):  # same as save()
        query = """INSERT INTO users (first_name, last_name, email, user_level, employee_id, password)
                VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(user_level)s, %(employee_id)s, %(password)s);"""
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * FROM users
                WHERE id = %(id)s;"""
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_by_email(cls, data):
        query = """SELECT * FROM users
                WHERE email = %(email)s;"""
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_employee_id(cls, data):
        query = """SELECT * FROM users WHERE employee_id = %(employee_id)s;"""
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_all_users(cls):
        query = """SELECT * FROM users;"""
        results = connectToMySQL(DB).query_db(query)
        all_users = []
        for user in results:
            all_users.append(cls(user))
        return all_users

    @property
    def is_admin(self):
        return self.user_level == 9

    @classmethod
    def get_one_user(cls, data):
        query = """SELECT * FROM users
                WHERE id = %(id)s"""
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            one_user = cls(results[0])
            return one_user
        return results
    
    @classmethod
    def update_last_logged_on(cls, id):
        query = """UPDATE users SET last_logged_on = NOW() WHERE id = %(id)s;"""
        data = {"id" : id}
        results = connectToMySQL(DB).query_db(query, data)
        print(data)
        print(results)
        return results
    
    def get_last_logged_on(self):
        return self.last_logged_on
    
    @classmethod
    def update(cls, data):
        query = """
                UPDATE users
                SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, 
                WHERE id = %(id)s;
        """
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM users WHERE id = %(id)s"
        results = connectToMySQL(DB).query_db(query, {'id' : id})
        return results

    @staticmethod
    def validate_data(data):
        is_valid = True
        if len(data["first_name"]) < 1:
            is_valid = False
            flash("First name required", "registration")
        elif len(data["first_name"]) < 2:
            is_valid = False
            flash("First name must be at least 2 characters", "registration")
        elif not ALPHA.match(data["first_name"]):
            is_valid = False
            flash("First name must be letters only", "registration")
        if len(data["last_name"]) < 1:
            is_valid = False
            flash("Last name required", "registration")
        elif len(data["last_name"]) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters", "registration")
        elif not ALPHA.match(data["last_name"]):
            is_valid = False
            flash("Last name must be letters only", "registration")
        if len(data["email"]) < 1:
            is_valid = False
            flash("Email required", "registration")  # do email at the end
        elif not EMAIL_REGEX.match(data["email"]):
            is_valid = False
            flash("Email must be a valid format", "registration")
        else:
            user_data = {"email": data["email"], "employee_id": data["employee_id"]}
            potential_user = User.get_by_email(user_data)
            potential_employee = User.get_by_employee_id(user_data)
            if potential_user:
                flash("Email already exists!", "registration")
                is_valid = False
            if potential_employee:
                flash("Employee ID already exists!", "registration")
                is_valid = False
        if len(data["password"]) < 1:
            is_valid = False
            flash("Password required", "registration")
        elif len(data["password"]) < 3:
            is_valid = False
            flash("Password must be at least 3 characters", "registration")
        elif data["password"] != data["confirm_password"]:
            is_valid = False
            flash("Password does not match!", "registration")
        elif not ALPHANUMERIC.match(data["password"]):
            is_valid = False
            flash(
                "Password must have at least one number and one Uppercase letter",
                "registration",
            )
        if data["user_level"] == "-1":
            is_valid = False
            flash("Please select a user level", "registration")

        return is_valid
