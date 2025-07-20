from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from Database.dbConnection import db, connect_db

# Flask app setup
app = Flask(__name__, template_folder='templates')
app.secret_key = "your_secret_key"

connect_db(app)

# Import models
from Models.projectModel import Project
from Models.assetInformationModel import AssetInformation
from Models.assetRiskModel import AssetRisk
from Models.impactPriorityModel import ImpactPriority
from Models.riskMitigationModel import RiskMitigation
from Models.assetContainerModel import AssetContainer


@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/stepOne', methods=['GET', 'POST'])
def step_one():
    if request.method == 'POST':
        # Create a new project entry with the project title
        project_title = request.form.get('project-title')
        project_id = Project.insert_project(project_title)

        # Insert asset information linked to the project
        asset_id = AssetInformation.insert_asset_profile(
            project_id=project_id,
            critical_asset=request.form.get('critical-asset'),
            rationale_for_selection=request.form.get('rationale'),
            description=request.form.get('description'),
            owners=request.form.get('owner'),
            confidentiality=request.form.get('confidentiality'),
            integrity=request.form.get('integrity'),
            availability=request.form.get('availability'),
            most_important_security_requirement=request.form.get('most-important-security')
        )

        # Store project and asset IDs in session for later steps
        session['project_id'] = project_id
        session['asset_id'] = asset_id

        return redirect(url_for('step_two'))

    return render_template('stepOne.html')


@app.route('/stepTwo', methods=['GET', 'POST'])
def step_two():
    if 'project_id' not in session:
        return redirect(url_for('step_one'))
    
    if request.method == 'POST':
        ImpactPriority.insert_priority(
            project_id=session['project_id'],
            reputation_confidence=request.form.get('reputation'),
            financial=request.form.get('finance'),
            productivity=request.form.get('productivity'),
            safety_health=request.form.get('safety'),
            fines_legal_penalties=request.form.get('fines')
        )
        return redirect(url_for('step_three'))
    return render_template('stepTwo.html')

@app.route('/stepThree', methods=['GET', 'POST'])
def step_three():
    if 'project_id' not in session:
        return redirect(url_for('step_two'))
    
    if request.method == 'POST':
        AssetContainer.insert_container(
            project_id=session['project_id'],
            asset_id=session['asset_id'],
            owners=request.form.get('owners'),
            technical_internal=request.form.get('technical-internal'),
            technical_external=request.form.get('technical-external'),
            physical_internal=request.form.get('physical-internal'),
            physical_external=request.form.get('physical-external'),
            people_internal=request.form.get('people-internal'),
            people_external=request.form.get('people-external')
        )
        return redirect(url_for('step_four'))
    return render_template('stepThree.html')

@app.route('/stepFour', methods=['GET', 'POST'])
def step_four():
    if 'project_id' not in session:
        return redirect(url_for('step_three'))
    
    # Retrieve impact priorities from Step 2
    impact_priorities = ImpactPriority.get_priority_by_project_id(session['project_id'])

    if request.method == 'POST':
        AssetRisk.insert_risk({
            'project_id': session['project_id'],
            'asset_id': session['asset_id'],
            'area_of_concern': request.form.get('area-of-concern'),
            'actor': request.form.get('actor'),
            'means': request.form.get('means'),
            'motive': request.form.get('motive'),
            'outcome': request.form.get('outcome'),
            'security_requirements': request.form.get('security-requirements'),
            'probability': request.form.get('probability'),
            'consequences': request.form.get('consequences'),
            'financial': request.form.get('financial'),
            'productivity': request.form.get('productivity'),
            'safety_health': request.form.get('safety_health'),
            'fines_legal_penalties': request.form.get('fines'),
            'relative_score': request.form.get('relative_score')
        })
        return redirect(url_for('step_five'))
    return render_template('stepFour.html', impact_priorities=impact_priorities)

@app.route('/stepFive', methods=['GET', 'POST'])
def step_five():
    if 'project_id' not in session:
        return redirect(url_for('step_four'))

    # Fetch the relevant risk_id (assumed logic to fetch the correct risk_id)
    project = Project.query.get(session['project_id'])
    risk_id = project.asset_risks[0].id  # Just an example; use appropriate logic to find the correct risk

    if request.method == 'POST':
        RiskMitigation.insert_risk_mitigation({
            'project_id': session['project_id'],
            'risk_id': risk_id,  # Assign the correct risk_id dynamically
            'technical_mitigation': request.form.get('technical-mitigation'),
            'physical_mitigation': request.form.get('physical-mitigation'),
            'people_mitigation': request.form.get('people-mitigation')
        })
        return redirect(url_for('dashboard'))

    return render_template('stepFive.html', risk_id=risk_id)


@app.route('/dashboard')
def dashboard():
    projects = Project.query.all()
    assets = AssetInformation.query.all()
    asset_risks = AssetRisk.query.all()
    impact_priorities = ImpactPriority.query.all()  # Fetch all impact priorities

    # Convert SQLAlchemy objects to dictionaries
    assets_data = [
        {
            "id": asset.id,
            "project_id": asset.project_id,
            "critical_asset": asset.critical_asset,
            "description": asset.description,
        }
        for asset in assets
    ]

    asset_risks_data = [
        {
            "id": risk.id,
            "project_id": risk.project_id,
            "asset_id": risk.asset_id,
            "area_of_concern": risk.area_of_concern,
            "actor": risk.actor,
            "means": risk.means,
            "motive": risk.motive,
            "outcome": risk.outcome,
            "security_requirements": risk.security_requirements,
            "probability": risk.probability,
            "consequences": risk.consequences,
            "relative_score": risk.relative_score,
        }
        for risk in asset_risks
    ]

    impact_priorities_data = [
        {
            "id": priority.id,
            "project_id": priority.project_id,
            "reputation_confidence": priority.reputation_confidence,
            "financial": priority.financial,
            "productivity": priority.productivity,
            "safety_health": priority.safety_health,
            "fines_legal_penalties": priority.fines_legal_penalties,
        }
        for priority in impact_priorities
    ]

    return render_template(
        'dashboard.html',
        projects=projects,
        assets=assets_data,  
        asset_risks=asset_risks_data,
        impact_priorities=impact_priorities_data,  # Pass serialized impact priorities
        total_projects=len(projects),
        total_assets=len(assets),
        total_risks=len(asset_risks),
    )

@app.route('/addAsset', methods=['GET', 'POST'])
def add_asset():
    project_id = request.args.get('project_id')

    if not project_id:
        return redirect(url_for('dashboard'))  # Redirect if no project is selected

    # Fetch impact priorities
    impact_priority_obj = ImpactPriority.get_priority_by_project_id(project_id)
    if not impact_priority_obj:
        return "Error: Impact Priority not found for this project.", 400  # Handle missing data

    # Convert ImpactPriority object to a dictionary for JSON serialization
    impact_priority = {
        'financial': impact_priority_obj.financial,
        'productivity': impact_priority_obj.productivity,
        'safety_health': impact_priority_obj.safety_health,
        'fines_legal_penalties': impact_priority_obj.fines_legal_penalties
    }

    if request.method == 'POST':
        # Insert new asset information
        asset_id = AssetInformation.insert_asset_profile(
            project_id=project_id,
            critical_asset=request.form.get('critical-asset'),
            rationale_for_selection=request.form.get('rationale'),
            description=request.form.get('description'),
            owners=request.form.get('owners'),
            confidentiality=request.form.get('confidentiality'),
            integrity=request.form.get('integrity'),
            availability=request.form.get('availability'),
            most_important_security_requirement=request.form.get('most-important-security')
        )

        # Insert asset container details
        AssetContainer.insert_container(
            project_id=project_id,
            asset_id=asset_id,
            owners=request.form.get('owners'),
            technical_internal=request.form.get('technical-internal'),
            technical_external=request.form.get('technical-external'),
            physical_internal=request.form.get('physical-internal'),
            physical_external=request.form.get('physical-external'),
            people_internal=request.form.get('people-internal'),
            people_external=request.form.get('people-external')
        )

        # User-selected severity levels (Low, Medium, High)
        severity_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
        financial = request.form.get('financial')
        productivity = request.form.get('productivity')
        safety_health = request.form.get('safety_health')
        fines_legal_penalties = request.form.get('fines')

        # Convert severity levels to numerical values (default to 1 if empty)
        financial_score = severity_mapping.get(financial, 1)
        productivity_score = severity_mapping.get(productivity, 1)
        safety_health_score = severity_mapping.get(safety_health, 1)
        fines_legal_penalties_score = severity_mapping.get(fines_legal_penalties, 1)

        # Calculate relative score based on impact priority values
        relative_score = (
            (int(impact_priority['financial']) * financial_score) +
            (int(impact_priority['productivity']) * productivity_score) +
            (int(impact_priority['safety_health']) * safety_health_score) +
            (int(impact_priority['fines_legal_penalties']) * fines_legal_penalties_score)
        )

        # Insert asset risk details
        risk_id = AssetRisk.insert_risk({
            'project_id': project_id,
            'asset_id': asset_id,
            'area_of_concern': request.form.get('area-of-concern'),
            'actor': request.form.get('actor'),
            'means': request.form.get('means'),
            'motive': request.form.get('motive'),
            'outcome': request.form.get('outcome'),
            'security_requirements': request.form.get('security-requirements'),
            'probability': request.form.get('probability'),
            'consequences': request.form.get('consequences'),
            'financial': financial,
            'productivity': productivity,
            'safety_health': safety_health,
            'fines_legal_penalties': fines_legal_penalties,
            'relative_score': relative_score  # Use calculated relative score
        })

        # Insert risk mitigation strategies
        RiskMitigation.insert_risk_mitigation({
            'project_id': project_id,
            'risk_id': risk_id,
            'technical_mitigation': request.form.get('technical-mitigation'),
            'physical_mitigation': request.form.get('physical-mitigation'),
            'people_mitigation': request.form.get('people-mitigation')
        })

        return redirect(url_for('dashboard'))

    return render_template('addAsset.html', project_id=project_id, impact_priority=impact_priority)

@app.route('/deleteProject', methods=['DELETE'])
def delete_project():
    project_id = request.args.get('project_id')

    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

    # Delete all assets related to this project
    AssetRisk.query.filter_by(project_id=project_id).delete()
    AssetContainer.query.filter_by(project_id=project_id).delete()
    AssetInformation.query.filter_by(project_id=project_id).delete()
    RiskMitigation.query.filter_by(project_id=project_id).delete()
    ImpactPriority.query.filter_by(project_id=project_id).delete()
    
    # Delete the project itself
    project = Project.query.get(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        return jsonify({"message": "Project and all related assets deleted successfully"}), 200
    else:
        return jsonify({"error": "Project not found"}), 404


@app.route('/deleteAsset', methods=['DELETE'])
def delete_asset():
    asset_id = request.args.get('asset_id')

    if not asset_id:
        return jsonify({"error": "Asset ID is required"}), 400

    try:
        asset_id = int(asset_id)
    except ValueError:
        return jsonify({"error": "Invalid asset ID"}), 400

    # Step 1: Find all risks associated with the asset
    asset_risks = AssetRisk.query.filter_by(asset_id=asset_id).all()

    # Step 2: Delete all related risk mitigations first (to avoid foreign key errors)
    for risk in asset_risks:
        RiskMitigation.query.filter_by(risk_id=risk.id).delete()

    # Step 3: Delete all related asset risks
    AssetRisk.query.filter_by(asset_id=asset_id).delete()

    # Step 4: Delete asset containers linked to this asset
    AssetContainer.query.filter_by(asset_id=asset_id).delete()

    # Step 5: Delete the asset itself
    asset = AssetInformation.query.get(asset_id)
    if asset:
        db.session.delete(asset)
        db.session.commit()
        return jsonify({"message": "Asset and all related data deleted successfully"}), 200
    else:
        return jsonify({"error": "Asset not found"}), 404


if __name__ == '__main__':
    # Make sure to run within an application context
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
    