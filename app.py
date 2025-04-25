from flask import Flask, jsonify, request
from models import db, Drug, DrugInteraction, AdverseEvent, VaccineReaction, PrescriptionStat

from db_config import DB_URI, SQLITE_URI  # "?"
import os
import grpc
import public_health_pb2
import public_health_pb2_grpc
import threading
import time

import sqlalchemy.exc

# Initialize Flask app
app = Flask(__name__)

# Configure database tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Try PostgreSQL, fallback to SQLite
use_sqlite = False
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    with app.app_context():
        db.init_app(app)
        db.engine.connect()
    print("Connected to PostgreSQL database")
except sqlalchemy.exc.OperationalError as e:
    print(f"Failed to connect to PostgreSQL: {e}")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharma_app.db'
    use_sqlite = True
    with app.app_context():
        db.init_app(app)
    print("Using SQLite instead")

# Setup gRPC client
channel = grpc.insecure_channel('localhost:50051')
stub = public_health_pb2_grpc.PublicHealthStub(channel)

# Routes for database models
@app.route('/drugs', methods=['GET'])
def get_drugs():
    drugs = Drug.query.all()
    return jsonify([{'id': drug.id, 'name': drug.name} for drug in drugs])


@app.route('/drugs', methods=['POST'])
def add_drug():
    data = request.json
    new_drug = Drug(id=data['id'], name=data['name'])
    db.session.add(new_drug)
    db.session.commit()
    return jsonify({'message': 'Drug added successfully'}), 201

@app.route('/interactions', methods=['GET'])
def get_interactions():
    interactions = DrugInteraction.query.all()
    return jsonify([{
        'id': i.id,
        'drugA_id': i.drug_a_id,
        'drugB_id': i.drug_b_id,
        'interaction_type': i.interaction_type,
        'severity': i.severity
    } for i in interactions])

#@app.route('/prescriptions', methods=['GET'])
#def get_prescriptions():
    #prescriptions = Prescription.query.all()
    #return jsonify([{
      #  'id': p.id,
      # 'prescriber_name': p.prescriber_name,
      #  'drug_id': p.drug_id,
      #  'dosage': p.dosage
   # } for p in prescriptions])

@app.route('/feedback', methods=['POST'])
def add_feedback():
    data = request.json
    new_feedback = Feedback(
        user_email=data['user_email'],
        experience=data['experience'],
        timestamp=data['timestamp']
    )
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback added successfully'}), 201

# Routes for the public health monitoring service
@app.route('/adverse-events', methods=['GET'])
def get_adverse_events():
    try:
        response = stub.FetchAdverseEvents(public_health_pb2.Empty())
        return jsonify([{"substance_name": event.substance_name, "reaction": event.reaction}
                        for event in response.events])
    except grpc.RpcError:
        return jsonify({"error": "gRPC service unavailable"}), 503

@app.route('/vaccines/reactions', methods=['GET'])
def get_vaccine_reactions():
    try:
        response = stub.FetchVaccineReactions(public_health_pb2.Empty())
        return jsonify([{"vaccine_name": reaction.vaccine_name, "symptoms": reaction.symptoms}
                        for reaction in response.reactions])
    except grpc.RpcError:
        return jsonify({"error": "gRPC service unavailable"}), 503

@app.route('/prescription-stats', methods=['GET'])
def get_prescription_stats():
    try:
        response = stub.FetchPrescriptionStats(public_health_pb2.Empty())
        return jsonify([{"name": stat.name, "total_prescribed": stat.total_prescribed}
                        for stat in response.stats])
    except grpc.RpcError:
        return jsonify({"error": "gRPC service unavailable"}), 503

# Routes for the pharmacist support API (from OpenAPI spec)
@app.route('/api/pharmacist-support/drugs/interactions', methods=['GET'])
def get_drug_interactions():
    # Implementation for drug interactions endpoint
    return jsonify([
        {
            "drugA": "Warfarin",
            "drugB": "Aspirin",
            "severity": "High",
            "description": "Increased risk of bleeding"
        },
        {
            "drugA": "Simvastatin",
            "drugB": "Erythromycin",
            "severity": "Moderate",
            "description": "Increased risk of myopathy"
        }
    ])

@app.route('/api/pharmacist-support/drugs/alternatives', methods=['GET'])
def get_drug_alternatives():
    # Implementation for drug alternatives endpoint
    return jsonify([
        {
            "original_drug": "Atorvastatin",
            "alternatives": ["Rosuvastatin", "Pravastatin"],
            "reason": "Lower risk of muscle pain"
        },
        {
            "original_drug": "Ibuprofen",
            "alternatives": ["Acetaminophen", "Naproxen"],
            "reason": "Lower risk of GI bleeding"
        }
    ])

@app.route('/api/pharmacist-support/drugs/labeling', methods=['GET'])
def get_drug_labeling():
    # Implementation for drug labeling endpoint
    return jsonify([
        {
            "drug_name": "Metformin",
            "warnings": ["Lactic acidosis risk", "Not for use in severe kidney disease"],
            "dosage_info": "Start with 500mg twice daily with meals"
        },
        {
            "drug_name": "Lisinopril",
            "warnings": ["Angioedema risk", "Pregnancy category D"],
            "dosage_info": "Start with 10mg once daily"
        }
    ])


# Database initialization (creating tables and adding initial data)
with app.app_context():
    #db.init_app(app) # Ensure db is initialized with the current app config
    db.create_all()

    # Check if we need to add initial data
    if Drug.query.count() == 0:
        # Add some sample drugs
        sample_drugs = [
            Drug(id="DRUG001", name="Paracetamol"),
            Drug(id="DRUG002", name="Ibuprofen"),
            Drug(id="DRUG003", name="Amoxicillin"),
            Drug(id="DRUG004", name="Metformin")
        ]
        db.session.add_all(sample_drugs)

        # Add some sample interactions
        sample_interactions = [
            DrugInteraction(drug_a_id="DRUG001", drug_b_id="DRUG002",
                            interaction_type="Potentiation", severity="Moderate"),
            DrugInteraction(drug_a_id="DRUG002", drug_b_id="DRUG003",
                            interaction_type="Inhibition", severity="Mild")
        ]
        db.session.add_all(sample_interactions)

        db.session.commit()

# Function to start the gRPC server in a separate thread
def start_grpc_server():
    from public_health_server import serve
    serve()

if __name__ == '__main__':
    # Start gRPC server in a background thread
    grpc_thread = threading.Thread(target=start_grpc_server, daemon=True)
    grpc_thread.start()

    # Wait for the gRPC server to start
    time.sleep(2)

    # Run Flask app
    app.run(host='localhost', port=5000, debug=True)
