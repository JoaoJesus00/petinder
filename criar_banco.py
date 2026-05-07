from app import create_app, db
from werkzeug.security import generate_password_hash
import sqlite3

app = create_app()

with app.app_context():
    db.create_all()
    print('Tabelas criadas!')

    conn = sqlite3.connect('petinder.db')
    cursor = conn.cursor()

    # Estados
    cursor.execute("INSERT OR IGNORE INTO estado (id, nome, sigla) VALUES (1, 'São Paulo', 'SP')")
    cursor.execute("INSERT OR IGNORE INTO estado (id, nome, sigla) VALUES (2, 'Rio de Janeiro', 'RJ')")
    cursor.execute("INSERT OR IGNORE INTO estado (id, nome, sigla) VALUES (3, 'Minas Gerais', 'MG')")

    # Cidades
    cursor.execute("INSERT OR IGNORE INTO cidade (id, nome, id_estado) VALUES (1, 'Franco da Rocha', 1)")
    cursor.execute("INSERT OR IGNORE INTO cidade (id, nome, id_estado) VALUES (2, 'São Paulo', 1)")
    cursor.execute("INSERT OR IGNORE INTO cidade (id, nome, id_estado) VALUES (3, 'Campinas', 1)")
    cursor.execute("INSERT OR IGNORE INTO cidade (id, nome, id_estado) VALUES (4, 'Rio de Janeiro', 2)")
    cursor.execute("INSERT OR IGNORE INTO cidade (id, nome, id_estado) VALUES (5, 'Belo Horizonte', 3)")

    # Espécies
    cursor.execute("INSERT OR IGNORE INTO especie (id, nome) VALUES (1, 'Cão')")
    cursor.execute("INSERT OR IGNORE INTO especie (id, nome) VALUES (2, 'Gato')")

    # Raças de cães
    racas_caes = [
        'Labrador', 'Golden Retriever', 'Bulldog', 'Pastor Alemão',
        'Poodle', 'Shih Tzu', 'Yorkshire', 'Maltês', 'Beagle',
        'Dachshund', 'Pinscher', 'Rottweiler', 'Husky Siberiano',
        'Border Collie', 'Lhasa Apso', 'Sem Raça Definida'
    ]

    # Raças de gatos
    racas_gatos = [
        'Persa', 'Siamês', 'Maine Coon', 'Ragdoll', 'Bengal',
        'Angorá', 'British Shorthair', 'Sphynx', 'Scottish Fold',
        'Sem Raça Definida'
    ]

    for raca in racas_caes:
        cursor.execute("INSERT OR IGNORE INTO raca (nome, id_especie) VALUES (?, 1)", (raca,))

    for raca in racas_gatos:
        cursor.execute("INSERT OR IGNORE INTO raca (nome, id_especie) VALUES (?, 2)", (raca,))

    # Usuário admin
    senha_admin = generate_password_hash('admin123')
    cursor.execute("""
        INSERT OR IGNORE INTO usuario (id, nome, email, cpf, id_cidade, senha, plano)
        VALUES (1, 'Admin', 'admin@petinder.com', '00000000000', 1, ?, 'premium')
    """, (senha_admin,))

    # Usuário de teste
    senha_joao = generate_password_hash('1234')
    cursor.execute("""
        INSERT OR IGNORE INTO usuario (id, nome, email, cpf, id_cidade, senha, plano)
        VALUES (2, 'João', 'joao@email.com', '12345678901', 1, ?, 'free')
    """, (senha_joao,))

    # Usuário de teste 2
    senha_maria = generate_password_hash('1234')
    cursor.execute("""
        INSERT OR IGNORE INTO usuario (id, nome, email, cpf, id_cidade, senha, plano)
        VALUES (3, 'Maria', 'maria@email.com', '98765432100', 1, ?, 'free')
    """, (senha_maria,))

    # Pet de teste
    cursor.execute("""
        INSERT OR IGNORE INTO animal (id, nome, idade, genero, id_especie, id_usuario, pedigree)
        VALUES (1, 'Rex', 3, 'M', 1, 2, 0)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO animal (id, nome, idade, genero, id_especie, id_usuario, pedigree)
        VALUES (2, 'Bella', 24, 'F', 1, 3, 0)
    """)

    conn.commit()
    conn.close()
    print('Dados iniciais inseridos!')
    print('')
    print('=== USUÁRIOS DE TESTE ===')
    print('Admin:  admin@petinder.com / admin123')
    print('João:   joao@email.com / 1234')
    print('Maria:  maria@email.com / 1234')
    print('=========================')
    print('')
    print('Banco criado com sucesso! Rode python run.py para iniciar.')