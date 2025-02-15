from app import db

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(100), nullable=False)
    field_value = db.Column(db.String(100), nullable=False)
    field_description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"FormData('{self.field_name}', '{self.field_value}')"