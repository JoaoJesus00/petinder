# Modelo pro banco de dados dos Usuários

from app import db, login_manager # Importando as váriaveis do app/__init__.py
from flask_login import UserMixin # UserMixin traz funções prontas para o Flask Login
from werkzeug.security import generate_password_hash, check_password_hash # Funções prontas para lidar com senhas, elas embaralham as senhas antes de salvar para segurança em caso de invasão

class Usuario(UserMixin, db.Model):
    
    __tablename__ = 'usuario' # Diz ao SQL qual a tabela do banco esse modelo representa
    
    # Abaixo cada linha representa uma coluna da tabela no banco:
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    endereco = db.Column(db.String(100))
    id_cidade = db.Column(db.Integer, db.ForeignKey('cidade.id'), nullable=False) # Chave estrangeira
    senha = db.Column(db.String(255), nullable=False)
    plano = db.Column(db.String(10), default='free')
    
    # Relacionamentos:
    animais = db.relationship('Animal', backref='dono', lazy=True)
    notificacoes = db.relationship('Notificacao', backref='usuario', lazy=True)
    #backref cria o caminho inverso, lazy para buscar os dados só quando for realmente usar pra economizar memória
    
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha) # Recebe a senha, embaralha e salva
        
    def check_senha(self, senha):
        return check_password_hash(self.senha, senha) # Verifica se a senha bate com a salva
    
    def pode_adicionar_animal(self): # Regra de negócio: usuário free e premium
        if self.plano == 'premium': # Verifica se o usuário pode cadastrar mais animais baseado no plano dele
            return len(self.animais) < 10 # Se for premium pode até 10
        return len(self.animais) < 1 # Free pode até 1
    
    def __repr__(self): # Define de forma mais clara como o objeto aparece no terminal
        return f'<Usuario {self.email}>' # Modifica o texto que aparece
    
    @login_manager.user_loader # Avisa o FlaskLogin que essa a função abaixo é responsável por carregar usuários (decorador)
    def load_user(user_id): # Recebe o user_id salvo no cookie do navegador
        return Usuario.query.get(int(user_id)) # Verifica o usuário no banco pelo ID e devolve ele