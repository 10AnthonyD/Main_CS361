from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from services.recommendation_service import RecommendationService
import os


basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
recommender = RecommendationService(data_path='cleaned_games.csv')

def create_app():
    """Function to create and configure the flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Change this
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
    login_manager.init_app(app)

    from models.user import User


    # Import and register blueprints for modularity
    from routes.auth import auth_bp
    from routes.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()


    return app
