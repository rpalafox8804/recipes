from flask_app import app
from flask import render_template,redirect,request,session,flash
# point flask_app.models.PROJECT_IN_MODELS than import the class
from flask_app.models import recipe, user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# app routes go here 
@app.route('/')
def index():
    return render_template("registration_login.html")


@app.route('/register',methods=['POST'])
def create_user():
    user_in_db = user.User.email_validation(request.form)
    if user_in_db:
        flash("Please use another email, this is already in use", 'registration')
        return redirect("/")
    if not user.User.validate_user(request.form):
        return redirect('/')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    hashed_confirm_pass = bcrypt.generate_password_hash(request.form['confirm_password'])
    data = {
        "first_name":request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password":hashed_pass, 
        "confirm_password": hashed_confirm_pass
    }
    user_id = user.User.register(data)
    session['user_id'] = user_id
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    creds = { "email" : request.form["email"],
                "password" : request.form['password']
            }
    data = { "email" : request.form["email"] }
    if not user.User.validate_credentials(creds):
        return redirect('/')
    user_in_db = user.User.get_by_email(data)
    if not user_in_db:
        flash("Invalid credentials", 'login')
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db[0].password, request.form['password']):
        flash("Invalid credentials", 'login')
        return redirect('/')
    session['user_id'] = user_in_db[0].id
    return redirect ("/recipe")

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')