from flask import Flask
from Database.dbConnection import db, connect_db
from Models import Project, ImpactPriority, AssetInformation, AssetContainer, AssetRisk, RiskMitigation
from flask_migrate import Migrate

app = Flask(__name__)
connect_db(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    print("Database migration successful.")

if __name__ == "__main__":
    app.run(debug=True)