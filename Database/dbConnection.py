from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.url import URL

# Initialize SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/octave_srm'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        with app.app_context():
            db.create_all()
        print("Database connection successful.")
    except SQLAlchemyError as e:
        print(f"Error connecting to database: {e}")
