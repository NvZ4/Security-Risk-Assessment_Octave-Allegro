from Database.dbConnection import db

class ImpactPriority(db.Model):
    __tablename__ = 'impact_priorities'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    reputation_confidence = db.Column(db.Integer, nullable=False)
    financial = db.Column(db.Integer, nullable=False)
    productivity = db.Column(db.Integer, nullable=False)
    safety_health = db.Column(db.Integer, nullable=False)
    fines_legal_penalties = db.Column(db.Integer, nullable=False)

    project = db.relationship("Project", back_populates="impact_priorities")

    @staticmethod
    def insert_priority(project_id, reputation_confidence, financial, productivity, safety_health, fines_legal_penalties):
        priority = ImpactPriority(
            project_id=project_id,
            reputation_confidence=reputation_confidence,
            financial=financial,
            productivity=productivity,
            safety_health=safety_health,
            fines_legal_penalties=fines_legal_penalties
        )
        db.session.add(priority)
        db.session.commit()
        return priority.id

    @staticmethod
    def get_priority_by_id(priority_id):
        return ImpactPriority.query.filter_by(id=priority_id).first()

    @staticmethod
    def get_priority_by_project_id(project_id):
        return ImpactPriority.query.filter_by(project_id=project_id).first()
