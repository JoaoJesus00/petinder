# Configurações do projeto

import os # Biblioteca para trabalhar com o sistema operacional: criar pastas, ler arquivos, etc.

basedir = os.path.abspath(os.path.dirname(__file__)) # Puxa o local do projeto no computador e converte para o caminho completo

class Config:
    SECRET_KEY = 'petinder-chave-secreta-2026' # Chave para proteção
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'petinder.db') # Puxa onde está o banco de dados
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desativa um sistema do SQLAlchemy que consome memória desnecessária
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads') # Define a pasta onde as fotos dos pets serão salvas
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # Limita o tamanho máximo de arquivos que podem ser enviados para o servidor pra evitar sobrecarga