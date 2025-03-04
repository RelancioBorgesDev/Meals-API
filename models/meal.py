from database import db
from flask_login import UserMixin

class Meal(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    is_in_diet = db.Column(db.Boolean, nullable=False)
    # Chave estrangeira para User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # Relacionamento com User
    user = db.relationship("User", back_populates="meals")