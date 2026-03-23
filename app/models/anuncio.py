from app import db
from datetime import datetime

class Anuncio(db.Model):

    __tablename__ = 'anuncio'

    id = db.Column(db.Integer, primary_key=True)
    nome_anunciante = db.Column(db.String(150), nullable=False)
    imagem_url = db.Column(db.String(500), nullable=False) # Endereço da imagem do anúncio
    link_url = db.Column(db.String(500), nullable=False) # Pra onde o usuário vai quando clicar 
    ativo = db.Column(db.Integer, default=1)
    criado_em = db.Column(db.Text, nullable=False, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def ativar(self): # Ativa anúncio
        self.ativo = 1

    def desativar(self): # Desativa sem precisar deletar
        self.ativo = 0

    def esta_ativo(self):
        return self.ativo == 1

    def __repr__(self):
        return f'<Anuncio {self.nome_anunciante}>'