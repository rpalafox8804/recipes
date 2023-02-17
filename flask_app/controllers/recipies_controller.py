from flask_app import app
from flask import render_template,redirect,request,session,flash
# point flask_app.models.PROJECT_IN_MODELS than import the file
from flask_app.models import user, recipe
from flask_bcrypt import Bcrypt
from datetime import datetime
bcrypt = Bcrypt(app)

# app routes go here 
@app.route('/recipe')
def recipie_home():
    if 'user_id' in session:
        return render_template("recipe.html", user_info = user.User.get_by_id(session), recipe= recipe.Recipe.get_all())
    return redirect ('/')

@app.route('/recipe/new')
def recipe_new():
    if 'user_id' in session:
        return render_template("new_recipe.html")
    return redirect ('/')


@app.route('/recipie/create',methods=['POST'])
def create():
    # print(request.form)
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    data = {
        "name":request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_cooked": request.form['date_cooked'],
        "under_thirty": request.form['under_thirty'],
        "users_id": session['user_id'], 
        
    }
    recipe.Recipe.create(data)
    return redirect('/recipe')

@app.route('/recipe/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    recipe_dict = {
        "id" : recipe_id
    }
    recipe_info = recipe.Recipe.get_id(recipe_dict)
    session['name'] = recipe_info['name']    
    session['description'] = recipe_info['description']    
    session['instructions'] = recipe_info['instructions']    
    session['date_cooked'] = recipe_info['date_cooked']    
    session['under_thirty'] = recipe_info['under_thirty']    
    if 'user_id' in session:
        return render_template('edit_recipe.html', rec_id = recipe_id)
    return redirect ('/')

@app.route('/recipe/update/<int:recipe_id>', methods = ['POST'])
def update(recipe_id):
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(f'/recipe/edit/{recipe_id}')
    data = {
        "id" : recipe_id,
        "name":request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_cooked": request.form['date_cooked'],
        "under_thirty": request.form['under_thirty'],
        "users_id": session['user_id'], 
        
    }
    if 'user_id' in session:
        recipe.Recipe.update(data)
        return redirect('/recipe')
    return redirect('/')

@app.route('/recipe/delete/<int:recipe_id>')
def remove_recipe(recipe_id):
    data ={
        'id': recipe_id
    }
    if 'user_id' in session:
        recipe.Recipe.destroy(data)
        return redirect('/recipe')
    return redirect('/')

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):

    data ={
        'id': recipe_id
    }
    recipe_date = recipe.Recipe.get_one_recipe(data)
    date =recipe_date[0].date_cooked.strftime("%B %d, %Y" )
    if 'user_id' in session:
        return render_template("show_recipe.html", user_info = user.User.get_by_id(session), recipe_data = recipe.Recipe.get_one_recipe(data), recipe_date_made = date)
    return redirect ('/')
    # return render_template('show_recipe.html', recipe_data = recipe.Recipe.get_one_recipe(data))