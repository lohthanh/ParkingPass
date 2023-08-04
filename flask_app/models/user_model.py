from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
import re
from flask import flash



ALPHA = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
ALPHANUMERIC = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.user_level = data['user_level']
        self.employee_id = data['employee_id']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create(cls, data): #same as save()
        query = """INSERT INTO users (first_name, last_name, email, user_level, employee_id, password)
                VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(user_level)s, %(employee_id)s, %(password)s );"""
        results = connectToMySQL(DB).query_db(query, data)
        return results
    
    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * FROM users
                WHERE id = %(id)s;"""
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls (results[0])
        return False
    
    @classmethod
    def get_by_email(cls, data):
        query = """SELECT * FROM users
                WHERE email = %(email)s;"""
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls (results[0])
        return False
    
    @classmethod
    def get_all_users(cls, data):
        query = """SELECT * FROM users;"""
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls (results[0])
        return False
    
    @property
    def is_admin(self):
        return self.user_level == 9
    
    @classmethod
    def get_by_user_level(cls, data):
        query = """SELECT * FROM users WHERE user_level = %(user_level)s;"""
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            return cls (results[0])
        return False


    @staticmethod
    def validate_data (data):
        is_valid = True
        if len(data['first_name']) < 1:
            is_valid = False
            flash ('First name required', 'registration')
        elif len(data['first_name']) < 2:
            is_valid = False
            flash ('First name must be at least 2 characters', 'registration')
        elif not ALPHA.match(data['first_name']):
            is_valid = False
            flash ('First name must be letters only', 'registration')
        if len(data['last_name']) < 1:
            is_valid = False
            flash ('Last name required', 'registration')
        elif len(data['last_name']) < 2:
            is_valid = False
            flash ('Last name must be at least 2 characters', 'registration')
        elif not ALPHA.match(data['last_name']):
            is_valid = False
            flash ('Last name must be letters only', 'registration')
        if len(data['email']) < 1:
            is_valid = False
            flash('Email required', 'registration')  #do email at the end
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Email must be a valid format', 'registration')
        else:
            user_data = {
                'email' : data['email']
            }
            potiential_user = User.get_by_email(user_data)
            if potiential_user:
                flash ('Email already exists!', 'registration')
                is_valid = False
        if len(data['password']) < 1:
            is_valid = False
            flash ('Password required', 'registration')
        elif len(data['password']) < 3:
            is_valid = False
            flash ('Password must be at least 3 characters', 'registration')
        elif data['password'] != data['confirm_password']:
            is_valid = False
            flash ('Password does not match!', 'registration')
        elif not ALPHANUMERIC.match(data['password']):
            is_valid = False
            flash('Password must have at least one number and one Uppercase letter', 'registration')
        if data['user_level'] == '-1':
            is_valid = False
            flash ('Please select a user level', 'registration')
        
        return is_valid