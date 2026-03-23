from app import db
from datetime import datetime

class Match(db.Model):
    
    __tablename__ = 'match'
    
    # Colunas:
    id = db.Column(db.Integer, primary_key=True)
    id_animal_1 = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False) # Chave estrangeira
    id_animal_2 = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False) # Chave estrangeira
    data = db.Column(db.Text, nullable=False, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S')) # Data formatada
    # O match recebe dois animais da tabela animal para o match
    
    # Relacionamentos:
    # Aqui explicitamos qual campo corresponde a qual relacionamento, pois ambos apontam pra mesma tabela
    animal_1 = db.relationship('Animal', foreign_keys=[id_animal_1], backref='matches_feitos')
    animal_2 = db.relationship('Animal', foreign_keys=[id_animal_2], backref='matches_recebidos')
    
    def get_outro_animal(self, animal_id): # Essa função retorna a partir do id de um animal, o outro animal com quem ele fez o match
        if self.id_animal_1 == animal_id:
            return self.animal_2
        return self.animal_1
    
    def __repr__(self): # Define o texto que aparece para o objeto no terminal
        return f'<Match {self.id_animal_1} x {self.id_animal_2}>'