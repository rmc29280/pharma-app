from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Base model class
class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Drug model (COMBINED DEFINITION)
class Drug(BaseModel):
    __tablename__ = 'drugs'

    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    dosage_form = db.Column(db.String(50), nullable=True)
    strength = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(100), nullable=True)
    active_ingredients = db.relationship('ActiveIngredient', lazy=True)
    interactions_as_drug_a = db.relationship('DrugInteraction',
                                            foreign_keys='DrugInteraction.drug_a_id',
                                            backref='drug_a', lazy=True)
    interactions_as_drug_b = db.relationship('DrugInteraction',
                                            foreign_keys='DrugInteraction.drug_b_id',
                                            backref='drug_b', lazy=True)
    feedback = db.relationship('Feedback', backref='drug', lazy=True)

    def __repr__(self):
        return f'<Drug {self.name}>'

class ActiveIngredient(BaseModel):
    __tablename__ = 'active_ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    drug_id = db.Column(db.String(20), db.ForeignKey('drugs.id'), nullable=False)
    drug = db.relationship('Drug', backref=db.backref('ingredients', lazy=True))

    def __repr__(self):
        return f'<ActiveIngredient {self.name}>'

class DrugInteraction(db.Model):
    __tablename__ = 'drug_interactions'

    id = db.Column(db.Integer, primary_key=True)
    drug_a_id = db.Column(db.String(20), db.ForeignKey('drugs.id'), nullable=False)
    drug_b_id = db.Column(db.String(20), db.ForeignKey('drugs.id'), nullable=False)
    interaction_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    drug_id = db.Column(db.String(20), db.ForeignKey('drugs.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)

class AdverseEvent(db.Model):
    __tablename__ = 'adverse_events'

    id = db.Column(db.Integer, primary_key=True)
    substance_name = db.Column(db.String(100), nullable=False)
    reaction = db.Column(db.Text, nullable=False)

class VaccineReaction(db.Model):
    __tablename__ = 'vaccine_reactions'

    id = db.Column(db.Integer, primary_key=True)
    vaccine_name = db.Column(db.String(100), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)

class PrescriptionStat(db.Model):
    __tablename__ = 'prescription_stats'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_prescribed = db.Column(db.Integer, nullable=False)
