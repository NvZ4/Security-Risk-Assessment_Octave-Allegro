import sys
sys.path.append("../")
from Database.dbConnection import db

class AssetContainer(db.Model):
    __tablename__ = 'asset_containers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset_informations.id'), nullable=False)
    owners = db.Column(db.Text, nullable=False)
    technical_internal = db.Column(db.Text, nullable=False)
    technical_external = db.Column(db.Text, nullable=False)
    physical_internal = db.Column(db.Text, nullable=False)
    physical_external = db.Column(db.Text, nullable=False)
    people_internal = db.Column(db.Text, nullable=False)
    people_external = db.Column(db.Text, nullable=False)

    # Relationships
    project = db.relationship('Project', back_populates='asset_containers')
    asset_information = db.relationship('AssetInformation', backref='asset_containers')
    
    @staticmethod
    def insert_container(project_id, asset_id, owners, technical_internal, technical_external, 
                     physical_internal, physical_external, people_internal, people_external):
          container = AssetContainer(
              project_id=project_id,
              asset_id=asset_id,
              owners=owners,
              technical_internal=technical_internal,
              technical_external=technical_external,
              physical_internal=physical_internal,
              physical_external=physical_external,
              people_internal=people_internal,
              people_external=people_external
              )
          db.session.add(container)
          db.session.commit()
          return container.id
    
    @staticmethod
    def insert_container_batch(containers):
        db.session.add_all(containers)
        db.session.commit()
    
    @staticmethod
    def get_container_by_id(id):
        return db.session.get(AssetContainer, id)
    
    @staticmethod
    def get_container_by_asset_id(asset_id):
        return AssetContainer.query.filter_by(asset_id=asset_id).first()
    
    @staticmethod
    def get_all_containers_by_project_id(project_id):
        return AssetContainer.query.filter_by(project_id=project_id).all()
