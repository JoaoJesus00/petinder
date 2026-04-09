# Modelo pro banco de dados dos Animais

from app import db # Importa as ferramentas do banco de dados criadas em app/__init__.py

class Animal(db.Model): # db.Model transforma essa classe em uma tabela do banco de dados com diversas funções
    __tablename__ = 'animal'
    
    # Colunas:
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    idade = db.Column(db.Integer)
    genero = db.Column(db.String(1), nullable=False)
    foto = db.Column(db.String(255))
    raca = db.Column(db.String(100))
    pedigree = db.Column(db.Integer, default=0)
    descricao = db.Column(db.Text)
    id_especie = db.Column(db.Integer, db.ForeignKey('especie.id'), nullable=False) # Chave estrangeira
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False) # Chave estrangeira

    # Relacionamento: Atalho pra acessar a espécie do animal
    especie = db.relationship('Especie', backref='animais', lazy=True)

    def tem_pedigree(self): # Retorna True se tem pedigree
        return self.pedigree == 1
    
    def get_genero(self): # Retorna macho ou fêmea
        if self.genero == 'M':
            return 'Macho'
        return 'Fêmea'
    
    def get_foto(self): # Retorna o caminho da foto do animal
        if self.foto:
            return f'/static/uploads/{self.foto}'
        return '/static/img/pet-default.png' # Se não tem foto retorna uma imagem padrão
    
    def __repr__(self):
        return f'<Animal {self.nome}>'