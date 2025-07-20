import sys
sys.path.append("../")
from Database.dbConnection import db


class AssetRisk(db.Model):
    __tablename__ = 'asset_risks'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_informations.id'), nullable=False)
    area_of_concern = db.Column(db.String, nullable=False)
    actor = db.Column(db.String, nullable=False)
    means = db.Column(db.String, nullable=False)
    motive = db.Column(db.String, nullable=False)
    outcome = db.Column(db.String, nullable=False)
    security_requirements = db.Column(db.String, nullable=False)
    probability = db.Column(db.String, nullable=False)
    consequences = db.Column(db.String, nullable=False)
    financial = db.Column(db.Enum('High', 'Medium', 'Low'), nullable=False)
    productivity = db.Column(db.Enum('High', 'Medium', 'Low'), nullable=False)
    safety_health = db.Column(db.Enum('High', 'Medium', 'Low'), nullable=False)
    fines_legal_penalties = db.Column(db.Enum('High', 'Medium', 'Low'), nullable=False)
    relative_score = db.Column(db.Integer, nullable=False)

    project = db.relationship("Project", back_populates="asset_risks")
    asset_information = db.relationship("AssetInformation", back_populates="asset_risks")
    risk_mitigations = db.relationship("RiskMitigation", back_populates="asset_risks")

    @staticmethod
    def insert_risk(risk_data):
        risk = AssetRisk(**risk_data)
        db.session.add(risk)
        db.session.commit()
        return risk.id

    @staticmethod
    def insert_risk_batch(risks_data):
        risks = [AssetRisk(**data) for data in risks_data]
        db.session.add_all(risks)
        db.session.commit()

    @staticmethod
    def get_risk_by_id(risk_id):
        return db.session.query(AssetRisk).filter_by(id=risk_id).first()

    @staticmethod
    def get_all_risks_by_asset_id(asset_id):
        return db.session.query(AssetRisk).filter_by(asset_id=asset_id).all()

    @staticmethod
    def get_all_risks_by_project_id(project_id):
        return db.session.query(AssetRisk).filter_by(project_id=project_id).all()
