from app import db

class Raca(db.Model):

    __tablename__ = 'raca'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    id_especie = db.Column(db.Integer, db.ForeignKey('especie.id'), nullable=False)

    especie = db.relationship('Especie', backref='racas', lazy=True)

    def __repr__(self):
        return f'<Raca {self.nome}>'