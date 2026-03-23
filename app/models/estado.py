from app import db

class Estado(db.Model):

    __tablename__ = 'estado'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    sigla = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return f'<Estado {self.sigla}>'