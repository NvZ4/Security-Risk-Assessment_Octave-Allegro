from Database.dbConnection import db
from Models.assetContainerModel import AssetContainer
from Models.assetRiskModel import AssetRisk
from Models.riskMitigationModel import RiskMitigation

class AssetInformation(db.Model):
    __tablename__ = 'asset_informations'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    critical_asset = db.Column(db.String(255), nullable=False)
    rationale_for_selection = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    owners = db.Column(db.Text, nullable=False)
    confidentiality = db.Column(db.String(255), nullable=False)
    integrity = db.Column(db.String(255), nullable=False)
    availability = db.Column(db.String(255), nullable=False)
    most_important_security_requirement = db.Column(db.String(255), nullable=False)
    
    project = db.relationship('Project', back_populates='asset_informations')
    asset_risks = db.relationship('AssetRisk', back_populates='asset_information')
    
    @staticmethod
    def insert_asset_profile(project_id, critical_asset, rationale_for_selection, description, owners, 
                         confidentiality, integrity, availability, most_important_security_requirement):
          asset_information = AssetInformation(
              project_id=project_id,
              critical_asset=critical_asset,
              rationale_for_selection=rationale_for_selection,
              description=description,
              owners=owners,
              confidentiality=confidentiality,
              integrity=integrity,
              availability=availability,
              most_important_security_requirement=most_important_security_requirement
              )
          db.session.add(asset_information)
          db.session.commit()
          return asset_information.id
    
    @staticmethod
    def get_asset_information_by_id(id):
        return db.session.get(AssetInformation, id)
    
    @staticmethod
    def get_all_assets_by_project_id(project_id):
        return AssetInformation.query.filter_by(project_id=project_id).all()
    
    @staticmethod
    def delete_asset_by_asset_id(asset_id):
        asset = AssetInformation.get_asset_information_by_id(asset_id)
        if not asset:
            return None
    
    # Delete related containers
        AssetContainer.query.filter_by(asset_id=asset_id).delete()

    # Delete related risks and mitigations
        risks = AssetRisk.query.filter_by(asset_id=asset_id).all()
        for risk in risks:
            RiskMitigation.query.filter_by(risk_id=risk.id).delete()
            db.session.delete(risk)

    # Delete the asset itself
        db.session.delete(asset)
        db.session.commit()
        return asset_id
