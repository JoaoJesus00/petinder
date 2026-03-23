from app import db
from datetime import datetime

class Notificacao(db.Model):
    
    __tablename__ = 'notificacao'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    lida = db.Column(db.Integer, default=0) # Guarda se a notificação foi lida ou não
    data = db.Column(db.Text, nullable=False, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def marcar_como_lida(self): # Quando o usuário clica na notificação, chamamos esse método
        self.lida = 1

    def foi_lida(self): # Retorna True se foi lida, útil para o frontend
        return self.lida == 1

    def __repr__(self):
        return f'<Notificacao {self.id} para Usuario {self.id_usuario}>'    