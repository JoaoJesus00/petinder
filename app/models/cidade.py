from app import db

class Cidade(db.Model):

    __tablename__ = 'cidade'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)

    estado = db.relationship('Estado', backref='cidades', lazy=True)

    def __repr__(self):
        return f'<Cidade {self.nome}>'