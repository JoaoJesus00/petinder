# Arquivo de rotas para os html
# Tudo que tem a ver com o uso do site em geral
# Cuida de:
# Home/Dashboard
# Perfil do usuário
# Página de upgrade Premium
# Notificações
# Blueprint: agrupa todas as rotas para o acesso dentro do app

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.notificacao import Notificacao

main = Blueprint('main', __name__)  # Cria o Blueprint main

@main.route('/') # Endereços da rota home
@main.route('/home') # Os dois levam pra mesma página
@login_required # Protege a rota, só entra quem estiver logado
def home():
    from app.models.anuncio import Anuncio # Importa o modelo anuncio
    anuncios = Anuncio.query.filter_by(ativo=1).all() # Busca todos anuncios no banco
    return render_template('home.html', anuncios=anuncios) # Renderiza a home e passa a lista de anúncios

@main.route('/perfil', methods=['GET', 'POST']) # GET: vizualizar, POST: salvar alterações
@login_required
def perfil():
    from app.models.cidade import Cidade
    cidades = Cidade.query.all() # Busca todas as cidades pro select do formulário de edição do perfil
    if request.method == 'POST': # Executa esse if quando o usuário clica em salvar
        current_user.nome = request.form.get('nome') # Atualiza os dados
        current_user.endereco = request.form.get('endereco')
        current_user.id_cidade = request.form.get('id_cidade')
        db.session.commit() # Salva as mudanças no banco de dados
        flash('Perfil atualizado com sucesso!', 'success') 
        return redirect(url_for('main.perfil')) # Redireciona de volta para a página de perfil
    return render_template('perfil.html', cidades=cidades) # Se for só GET, só renderiza o perfil.html

@main.route('/notificacoes')
@login_required
def notificacoes():
    todas = Notificacao.query.filter_by(
        id_usuario=current_user.id
    ).order_by(Notificacao.id.desc()).all() # Filtra do banco pra mostrar só as notificações do usuário logado

    for n in todas: # Verifica as notificações lidas
        if not n.foi_lida():
            n.marcar_como_lida()
    db.session.commit()

    return render_template('notificacoes.html', notificacoes=todas) # Renderiza passando a lista

@main.route('/premium') # Página de upgrade pra Premium
@login_required
def premium():
    return render_template('premium.html')