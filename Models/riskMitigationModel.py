from Database.dbConnection import db

class RiskMitigation(db.Model):
    __tablename__ = 'risk_mitigations'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    risk_id = db.Column(db.Integer, db.ForeignKey('asset_risks.id'), nullable=False)
    technical_mitigation = db.Column(db.String, nullable=False)
    physical_mitigation = db.Column(db.String, nullable=False)
    people_mitigation = db.Column(db.String, nullable=False)

    project = db.relationship("Project", back_populates="risk_mitigations")
    asset_risks = db.relationship("AssetRisk", back_populates="risk_mitigations")

    @staticmethod
    def insert_risk_mitigation(mitigation_data):
        mitigation = RiskMitigation(**mitigation_data)
        db.session.add(mitigation)
        db.session.commit()
        return mitigation.id

    @staticmethod
    def get_mitigation_by_id(mitigation_id):
        return RiskMitigation.query.filter_by(id=mitigation_id).first()

    @staticmethod
    def get_all_mitigations_by_project_id(project_id):
        return RiskMitigation.query.filter_by(project_id=project_id).all()

    @staticmethod
    def get_mitigation_by_risk_id(risk_id):
        return RiskMitigation.query.filter_by(risk_id=risk_id).first()
