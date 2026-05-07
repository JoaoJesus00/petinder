from app import db
from datetime import datetime

class Curtida(db.Model):

    __tablename__ = 'curtida'

    id = db.Column(db.Integer, primary_key=True)
    id_animal_de = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    id_animal_para = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    data = db.Column(db.Text, nullable=False, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    animal_de = db.relationship('Animal', foreign_keys=[id_animal_de], backref='curtidas_dadas')
    animal_para = db.relationship('Animal', foreign_keys=[id_animal_para], backref='curtidas_recebidas')

    def __repr__(self):
        return f'<Curtida {self.id_animal_de} -> {self.id_animal_para}>'