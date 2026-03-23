from app import db

class Especie(db.Model):

    __tablename__ = 'especie'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Especie {self.nome}>'

# Essa tabela é bem simples por que a tabela só guarda o nome das espécies e o id