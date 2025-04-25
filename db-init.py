from models import db, Drug, DrugInteraction, Prescription, Feedback
from datetime import datetime

def init_db():
    # Create tables
    db.create_all()
    
    # Check if data already exists
    if Drug.query.count() > 0:
        print("Database already contains data. Skipping initialization.")
        return
    
    # Add sample drugs
    drugs = [
        Drug(id="D001", drug_name="Paracetamol"),
        Drug(id="D002", drug_name="Ibuprofen"),
        Drug(id="D003", drug_name="Amoxicillin"),
        Drug(id="D004", drug_name="Metformin"),
        Drug(id="D005", drug_name="Lisinopril"),
        Drug(id="D006", drug_name="Atorvastatin"),
        Drug(id="D007", drug_name="Simvastatin"),
        Drug(id="D008", drug_name="Warfarin"),
        Drug(id="D009", drug_name="Aspirin"),
        Drug(id="D010", drug_name="Erythromycin")
    ]
    db.session.add_all(drugs)
    
    # Add drug interactions
    interactions = [
        DrugInteraction(drugA_id="D008", drugB_id="D009", interaction_type="Increased bleeding risk", severity="High"),
        DrugInteraction(drugA_id="D007", drugB_id="D010", interaction_type="Increases myopathy risk", severity="Moderate"),
        DrugInteraction(drugA_id="D001", drugB_id="D002", interaction_type="Enhanced analgesia", severity="Low"),
        DrugInteraction(drugA_id="D004", drugB_id="D005", interaction_type="Potentiates hypoglycemia", severity="Moderate")
    ]
    db.session.add_all(interactions)
    
    # Add prescriptions
    prescriptions = [
        Prescription(prescriber_name="Dr. John Smith", drug_id="D001", dosage="500mg 4x daily"),
        Prescription(prescriber_name="Dr. Jane Doe", drug_id="D003", dosage="250mg 3x daily"),
        Prescription(prescriber_name="Dr. Robert Johnson", drug_id="D004", dosage="1000mg 2x daily"),
        Prescription(prescriber_name="Dr. Emily Brown", drug_id="D006", dosage="20mg 1x daily")
    ]
    db.session.add_all(prescriptions)
    
    # Add feedback
    feedback = [
        Feedback(user_email="patient1@example.com", experience="Good experience with minimal side effects", 
                timestamp=datetime.now()),
        Feedback(user_email="patient2@example.com", experience="Mild nausea after taking medication", 
                timestamp=datetime.now())
    ]
    db.session.add_all(feedback)
    
    # Commit changes
    db.session.commit()
    print("Database initialized with sample data.")

if __name__ == "__main__":
    init_db()
