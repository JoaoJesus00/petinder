from app import create_app, db
from app.models.usuario import Usuario
from app.models.animal import Animal
from app.models.match import Match
from app.models.notificacao import Notificacao
from app.models.anuncio import Anuncio
from app.models.especie import Especie
from app.models.cidade import Cidade
from app.models.estado import Estado
from werkzeug.security import generate_password_hash
import sqlite3
import os

app = create_app()

with app.app_context():
    # Cria todas as tabelas
    db.create_all()
    print('Tabelas criadas!')

    # Insere dados iniciais
    conn = sqlite3.connect('petinder.db')
    cursor = conn.cursor()

    # Estado
    cursor.execute("INSERT OR IGNORE INTO estado (id, nome, sigla) VALUES (1, 'São Paulo', 'SP')")

    # Cidade
    cursor.execute("INSERT OR IGNORE INTO cidade (id, nome, id_estado) VALUES (1, 'Franco da Rocha', 1)")

    # Espécies
    cursor.execute("INSERT OR IGNORE INTO especie (id, nome) VALUES (1, 'Cão')")
    cursor.execute("INSERT OR IGNORE INTO especie (id, nome) VALUES (2, 'Gato')")

    # Usuário admin de teste
    senha_hash = generate_password_hash('1234')
    cursor.execute("""
        INSERT OR IGNORE INTO usuario (id, nome, email, cpf, id_cidade, senha, plano)
        VALUES (1, 'João', 'joao@email.com', '12345678901', 1, ?, 'free')
    """, (senha_hash,))

    conn.commit()
    conn.close()
    print('Dados iniciais inseridos!')
    print('Banco criado com sucesso!')