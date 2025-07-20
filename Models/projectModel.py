from Database.dbConnection import db
from Models.impactPriorityModel import ImpactPriority
from Models.assetInformationModel import AssetInformation
from Models.assetRiskModel import AssetRisk
from Models.riskMitigationModel import RiskMitigation
from Models.assetContainerModel import AssetContainer

class Project(db.Model):
    __tablename__ = 'projects'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

    impact_priorities = db.relationship("ImpactPriority", back_populates="project")
    asset_informations = db.relationship("AssetInformation", back_populates="project")
    asset_risks = db.relationship("AssetRisk", back_populates="project")
    risk_mitigations = db.relationship("RiskMitigation", back_populates="project")
    asset_containers = db.relationship("AssetContainer", back_populates="project", cascade="all, delete-orphan")

    @staticmethod
    def insert_project(title):
        if not title:
            raise ValueError("Title is required to create a project")
        
        project = Project(title=title)
        db.session.add(project)
        db.session.commit()
        return project.id

    @staticmethod
    def get_project_by_id(project_id):
        return Project.query.filter_by(id=project_id).first()

    @staticmethod
    def get_all_projects():
        return Project.query.all()

    @staticmethod
    def delete_project_by_id(project_id):
        # Delete related ImpactPriority
        prior = ImpactPriority.get_priority_by_project_id(project_id)
        if prior:
            db.session.delete(prior)

        # Delete related AssetInformation
        assets = AssetInformation.get_all_assets_by_project_id(project_id)
        for asset in assets:
            AssetInformation.delete_asset_by_id(asset.id)

        # Delete related AssetRisks
        risks = AssetRisk.get_all_risks_by_project_id(project_id)
        for risk in risks:
            db.session.delete(risk)

        # Delete related RiskMitigations
        mitigations = RiskMitigation.get_all_mitigations_by_project_id(project_id)
        for mitigation in mitigations:
            db.session.delete(mitigation)

        # Delete related AssetContainers
        containers = AssetContainer.get_all_containers_by_project_id(project_id)
        for container in containers:
            db.session.delete(container)

        # Delete the Project itself
        project = Project.get_project_by_id(project_id)
        if project:
            db.session.delete(project)

        db.session.commit()