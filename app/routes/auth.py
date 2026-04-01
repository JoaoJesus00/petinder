# Arquivo de rotas para os html
# Tudo a ver com identidade do usuário
# Responsabilidades:
# Página de cadastro
# Página de login
# Logout
# Blueprint: agrupa todas as rotas para o acesso dentro do app
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.usuario import Usuario
from app.models.especie import Especie
from datetime import datetime
# Criação do Blueprint:
auth = Blueprint('auth', __name__) 

# ROTA DE LOGIN:
@auth.route('/login', methods=['GET', 'POST']) # Liga o endereço /login a função abaixo e define os dois tipos de requisição aceitas pela rota: GET para acessar a página, e POST para enviar os dados
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('main.home')) # Se o usuário ja estiver logado redireciona pra home
    usuario = None
    if request.method == 'POST': # Se o usuário clica pra enviar o formulário entra nesse bloco
        email = request.form.get('email')
        senha = request.form.get('senha') # Pega os dados
        usuario = Usuario.query.filter_by(email=email).first() # Faz a busca no banco de dados

        if usuario and usuario.check_senha(senha): # Verifica se encontrou o email e se a senha bate com a salva
                login_user(usuario) # Efetiva o login
                flash(f'Bem-vindo de volta, {usuario.nome}!', 'success') # Envia mensagem de boas-vindas
                return redirect(url_for('main.home')) # Manda o usuário pra home
        else:
            flash('Email ou senha incorretos!', 'danger') # Se email ou senha incorretos, mensagem de erro

    return render_template('login.html') # Essa linha só executa se o usuário acessou a página de login (GET), ou se o login falhou

# ROTA DE CADASTRO:
@auth.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    from app.models.usuario import Usuario # Impoetamos aqui dentro para evitar conflito (importação circular)
    from app.models.especie import Especie
    from app.models.cidade import Cidade
    cidades = Cidade.query.all() # Busca todas as cidades do banco para o <select> do HTML
    
    if request.method == 'POST': # Abaixo pega todos os dados do formulário de cadastro
        nome = request.form.get('nome')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        endereco = request.form.get('endereco')
        id_cidade = request.form.get('id_cidade')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        if senha != confirmar_senha: # Verifica se o usuário digitou a mesma senha nos dois campos
            flash('As senhas não coincidem!', 'danger') # Se não, mostra mensagem de erro
            return render_template('cadastro.html', cidades=cidades) # E retorna para o formulário

        if Usuario.query.filter_by(email=email).first(): # Verifica se o email já existe no banco
            flash('Este email já está cadastrado!', 'danger') # Não pode haver duplicidade
            return render_template('cadastro.html', cidades=cidades)
        
        if Usuario.query.filter_by(cpf=cpf).first(): # Verifica se o CPF já existe no banco
            flash('Este CPF já está cadastrado!', 'danger')
            return render_template('cadastro.html', cidades=cidades)
        
        novo_usuario = Usuario(  # Se tudo estiver certo, cria um objeto Usuário com esses dados do formulário
            nome=nome,
            email=email,
            cpf=cpf,
            endereco=endereco,
            id_cidade=id_cidade,
            plano='free'
        )
        
        novo_usuario.set_senha(senha) # Chama o método que embaralha a senha antes de salvar
        
        db.session.add(novo_usuario) # Adiciona o usuário a fila de salvamento
        db.session.commit() # Confirma e salva tudo no banco de dados
        
        flash('Conta criada com sucesso! Faça login.', 'success') 
        return redirect(url_for('auth.login')) # Após criar conta, manda o usuário pro login com mensagem de sucesso

    return render_template('cadastro.html', cidades=cidades)

#ROTA DE LOGOUT:
@auth.route('/logout')
@login_required  # Se alguém tentar acessar essa pág sem estar logado, redireciona pra o login
def logout():
    logout_user() # Remove usuário da sessão
    flash('Você saiu da conta.', 'info') # Mensagem informativa
    return redirect(url_for('auth.login')) # Redireciona pro login