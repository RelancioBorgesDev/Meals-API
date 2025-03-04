from flask import Flask
from flask_login import LoginManager
from routes.meals import meals_bp
from routes.users import user_bp, login_manager
from database import db

app = Flask(__name__)

app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(meals_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

