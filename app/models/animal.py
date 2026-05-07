# Modelo pro banco de dados dos Animais

from app import db

class Animal(db.Model):

    __tablename__ = 'animal'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    idade = db.Column(db.Integer)
    genero = db.Column(db.String(1), nullable=False)
    foto = db.Column(db.String(255))
    pedigree = db.Column(db.Integer, default=0)
    descricao = db.Column(db.Text)
    id_especie = db.Column(db.Integer, db.ForeignKey('especie.id'), nullable=False)
    id_raca = db.Column(db.Integer, db.ForeignKey('raca.id'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    especie = db.relationship('Especie', backref='animais', lazy=True)
    raca = db.relationship('Raca', backref='animais', lazy=True)

    def tem_pedigree(self):
        return self.pedigree == 1

    def get_genero(self):
        if self.genero == 'M':
            return 'Macho'
        return 'Fêmea'

    def get_foto(self):
        if self.foto:
            return f'/static/uploads/{self.foto}'
        return '/static/img/pet-default.png'

    def __repr__(self):
        return f'<Animal {self.nome}>'