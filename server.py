# change BURGERS to name to connect to controller
from flask_app.controllers import users_controller, recipies_controller
from flask_app import app


if __name__ == "__main__":
    app.run(debug=True)