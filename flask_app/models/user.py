from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
mydb= 'recipie'

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL(mydb).query_db(query,data)

    @classmethod
    def get_id(cls,data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        users_from_db = connectToMySQL(mydb).query_db(query,data)
        return cls(users_from_db[0])
    
    @staticmethod
    def validate_credentials(user):
        is_valid = True
        if len(user['email']) < 1:
            flash("Please enter an email",'login')
            is_valid = False
        if len(user['password']) < 1:
            flash("Please enter a password",'login')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash("All fields required, please enter a First Name.",'registration')
            is_valid = False
        elif len(user['first_name']) < 2:
            flash("First Name needs to be longer.",'registration')
            is_valid = False
        if len(user['last_name']) < 1:
            flash("All fields required, please enter a Last Name.", 'registration')
            is_valid = False
        elif len(user['last_name']) < 2:
            flash("Last Name needs to be longer.",'registration')
            is_valid = False
        if len(user['email']) < 1:
            flash("All fields required, please enter an email.", 'registration')
            is_valid = False
        if len(user['password']) < 1:
            flash("All fields required, please enter a password.", 'registration')
            is_valid = False
        if len(user['confirm_password']) < 1:
            flash("All fields required, please enter a password.", 'registration')
            is_valid = False
        elif user['confirm_password'] != user['password']:
            flash("Passwords do not match.", 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'registration')
            is_valid = False
        
        return is_valid   
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(mydb).query_db(query,data)
        this_user = []
        if len(result) < 1:
            return False
        for r in result:
            this_user.append(cls(r))
        return this_user
    @classmethod 
    def email_validation(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(mydb).query_db(query,data)
        # print (result)
        return result 

    @classmethod
    def get_by_id(cls,session_id):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        # print (session_id)
        result = connectToMySQL(mydb).query_db(query,session_id)
        # print(result)
        # if len(result) < 1:
        #     return False
        return result
    # @classmethod
    # def save(cls,data):
    #     query = "INSERT INTO burgers (name,bun,meat,calories,created_at,updated_at) VALUES (%(name)s,%(bun)s,%(meat)s,%(calories)s,NOW(),NOW())"
    #     return connectToMySQL('burgers').query_db(query,data)

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM burgers;"
    #     burgers_from_db =  connectToMySQL('burgers').query_db(query)
    #     burgers =[]
    #     for b in burgers_from_db:
    #         burgers.append(cls(b))
    #     return burgers

    # @classmethod
    # def get_one(cls,data):
    #     query = "SELECT * FROM burgers WHERE burgers.id = %(id)s;"
    #     burger_from_db = connectToMySQL('burgers').query_db(query,data)

    #     return cls(burger_from_db[0])

    # @classmethod
    # def update(cls,data):
    #     query = "UPDATE burgers SET name=%(name)s, bun=%(bun)s, meat=%(meat)s, calories=%(calories)s,updated_at = NOW() WHERE id = %(id)s;"
    #     return connectToMySQL('burgers').query_db(query,data)

    # @classmethod
    # def destroy(cls,data):
    #     query = "DELETE FROM burgers WHERE id = %(id)s;"
    #     return connectToMySQL('burgers').query_db(query,data)
