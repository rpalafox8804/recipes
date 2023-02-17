from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
mydb= 'recipie'
class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name= data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_thirty = data['under_thirty']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def create(cls,data):
        query = "INSERT INTO recipes (name,description,instructions,date_cooked, under_thirty,users_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(date_cooked)s,%(under_thirty)s, %(users_id)s);"
        return connectToMySQL(mydb).query_db(query,data)

    @classmethod
    def get_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        recipe_from_db = connectToMySQL(mydb).query_db(query,data)
        return recipe_from_db[0]
    
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 1:
            flash("All fields required, please enter a Name.",'recipe')
            is_valid = False
        elif len(recipe['name']) < 3:
            flash("Please create a name longer than 3 characters.",'recipe')
            is_valid = False

        if len(recipe['description']) < 1:
            flash("All fields required, please enter a description.", 'recipe')
            is_valid = False
        elif len(recipe['description']) < 3:
            flash("Please create a description longer than 3 character.", 'recipe')
            is_valid = False

        if len(recipe['instructions']) < 1:
            flash("All fields required, please enter instructions.", 'recipe')
            is_valid = False
        elif len(recipe['instructions']) < 3:
            flash("Please create a description longer than 3 character.", 'recipe')
            is_valid = False

        if len(recipe['date_cooked']) < 1:
            flash("All fields required, please enter a date.", 'recipe')
            is_valid = False
        # print(recipe['under_thirty'])
        if len(recipe['under_thirty']) < 1:
            flash("All fields required, please select if the recipie can be prepared within 30 minutes.", 'recipe')
            is_valid = False
        # if not EMAIL_REGEX.match(user['email']): 
        #     flash("Invalid email address!", 'registration')
        #     is_valid = False
        return is_valid   
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(mydb).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    @classmethod
    def get_by_id(cls,session_id):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        print (session_id)
        result = connectToMySQL(mydb).query_db(query,session_id)
        return result
    @classmethod
    def get_one_recipe(cls, recipe_id):
        query = '''SELECT * 
                    FROM recipes left 
                    JOIN users 
                    ON users.id = recipes.users_id 
                    WHERE recipes.id = %(id)s;'''
        recipe_from_db =  connectToMySQL(mydb).query_db(query, recipe_id)
        recipe =[]
        for row in recipe_from_db:
            this_recipe = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'password' : row['password'],
                'email' : row['email'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'],
            }
            this_recipe.creator = user.User(user_data)
            recipe.append(this_recipe)
        return recipe



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes left JOIN users ON users.id = recipes.users_id;"
        recipe_from_db =  connectToMySQL(mydb).query_db(query)
        recipe =[]
        for row in recipe_from_db:
            this_recipe = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'password' : row['password'],
                'email' : row['email'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'],
            }
            this_recipe.creator = user.User(user_data)
            recipe.append(this_recipe)

        return recipe
    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s, under_thirty=%(under_thirty)s, date_cooked=%(date_cooked)s WHERE id = %(id)s;"
        return connectToMySQL(mydb).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(mydb).query_db(query,data)
    # @classmethod
    # def save(cls,data):
    #     query = "INSERT INTO burgers (name,bun,meat,calories,created_at,updated_at) VALUES (%(name)s,%(bun)s,%(meat)s,%(calories)s,NOW(),NOW())"
    #     return connectToMySQL('burgers').query_db(query,data)


    # @classmethod
    # def get_one(cls,data):
    #     query = "SELECT * FROM burgers WHERE burgers.id = %(id)s;"
    #     burger_from_db = connectToMySQL('burgers').query_db(query,data)

    #     return cls(burger_from_db[0])



#  @classmethod
#     def get_by_id(cls,session_id):
#         query = "SELECT * FROM users WHERE id = %(user_id)s;"
#         # print (session_id)
#         result = connectToMySQL(mydb).query_db(query,session_id)
#         # print(result)
#         # if len(result) < 1:
#         #     return False
#         return result