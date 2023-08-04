from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh this is a secret"
DB = 'employee_db'
