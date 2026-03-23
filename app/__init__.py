# Esse arquivo transforma a pasta <app> em um módulo pro Python reconhecer
# Puxa as configurações do config.py
# Além disso ele inicializa as funções que vão ser utilizadas
from flask import Flask # Framework que cria o site
from flask_sqlalchemy import SQLAlchemy # Ferramenta para conectar o Python ao banco de dados
from flask_login import LoginManager # Gerenciador de login e sessão
from flask_migrate import Migrate # Controla as mudanças no banco
from config import Config # Importa as configurações do config.py

db = SQLAlchemy()  # Cria as ferramentas do banco de dados
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app =  Flask(__name__) # Cria o app Flask
    
    app.config.from_object(Config) # Joga as configurações dentro do app
    
    db.init_app(app) # Conecta o banco de dados
    login_manager.init_app(app) # Conecta o sistema de login
    migrate.init_app(app, db) # Conecta o sistema de migrações ao app e ao banco
    
    login_manager.login_view = 'auth.login' # Configura o sistema de login
    login_manager.login_message = 'Faça login para acessar essa página.'
    login_manager.login_message_category = 'warning'

    from app.routes.auth import auth
    from app.routes.main import main
    # Blueprints para as rotas do app  
    app.register_blueprint(auth)
    app.register_blueprint(main)
    
    return app