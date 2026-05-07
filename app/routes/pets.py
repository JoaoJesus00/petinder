from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.animal import Animal
from app.models.especie import Especie
from app.models.raca import Raca
import os
from werkzeug.utils import secure_filename

pets = Blueprint('pets', __name__)

EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif'}

def arquivo_permitido(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

@pets.route('/meus-pets')
@login_required
def meus_pets():
    return render_template('meus_pets.html')

@pets.route('/novo-pet', methods=['GET', 'POST'])
@login_required
def novo_pet():
    especies = Especie.query.all()
    racas = Raca.query.all()

    if request.method == 'POST':
        nome = request.form.get('nome')
        idade = request.form.get('idade')
        genero = request.form.get('genero')
        id_especie = request.form.get('id_especie')
        id_raca = request.form.get('id_raca')
        pedigree = 1 if request.form.get('pedigree') else 0
        descricao = request.form.get('descricao')

        if not current_user.pode_adicionar_animal():
            flash(f'Você atingiu o limite de pets do seu plano!', 'warning')
            return redirect(url_for('main.premium'))

        foto_nome = None
        foto = request.files.get('foto')
        if foto and arquivo_permitido(foto.filename):
            from config import Config
            filename = secure_filename(foto.filename)
            foto_nome = f"{current_user.id}_{filename}"
            foto.save(os.path.join(Config.UPLOAD_FOLDER, foto_nome))

        novo = Animal(
            nome=nome,
            idade=idade,
            genero=genero,
            id_especie=id_especie,
            id_raca=id_raca,
            pedigree=pedigree,
            descricao=descricao,
            foto=foto_nome,
            id_usuario=current_user.id
        )

        db.session.add(novo)
        db.session.commit()

        flash(f'{nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('pets.meus_pets'))

    return render_template('novo_pet.html', especies=especies, racas=racas)

@pets.route('/editar-pet/<int:animal_id>', methods=['GET', 'POST'])
@login_required
def editar_pet(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    especies = Especie.query.all()
    racas = Raca.query.all()

    if animal.id_usuario != current_user.id:
        flash('Você não tem permissão para editar esse pet!', 'danger')
        return redirect(url_for('pets.meus_pets'))

    if request.method == 'POST':
        animal.nome = request.form.get('nome')
        animal.idade = request.form.get('idade')
        animal.genero = request.form.get('genero')
        animal.id_especie = request.form.get('id_especie')
        animal.id_raca = request.form.get('id_raca')
        animal.pedigree = 1 if request.form.get('pedigree') else 0
        animal.descricao = request.form.get('descricao')

        foto = request.files.get('foto')
        if foto and arquivo_permitido(foto.filename):
            from config import Config
            filename = secure_filename(foto.filename)
            foto_nome = f"{current_user.id}_{filename}"
            foto.save(os.path.join(Config.UPLOAD_FOLDER, foto_nome))
            animal.foto = foto_nome

        db.session.commit()
        flash('Pet atualizado com sucesso!', 'success')
        return redirect(url_for('pets.meus_pets'))

    return render_template('editar_pet.html', animal=animal, especies=especies, racas=racas)

@pets.route('/excluir-pet/<int:animal_id>')
@login_required
def excluir_pet(animal_id):
    animal = Animal.query.get_or_404(animal_id)

    if animal.id_usuario != current_user.id:
        flash('Você não tem permissão para excluir esse pet!', 'danger')
        return redirect(url_for('pets.meus_pets'))

    db.session.delete(animal)
    db.session.commit()
    flash('Pet removido com sucesso!', 'success')
    return redirect(url_for('pets.meus_pets'))

@pets.route('/buscar/<int:animal_id>', methods=['GET', 'POST'])
@login_required
def buscar(animal_id):
    from app.models.curtida import Curtida
    from app.models.match import Match

    animal = Animal.query.get_or_404(animal_id)

    if animal.id_usuario != current_user.id:
        flash('Você não tem permissão!', 'danger')
        return redirect(url_for('pets.meus_pets'))

    # Pega os filtros enviados pelo formulário
    filtro_genero = request.args.get('genero', '')
    filtro_raca = request.args.get('id_raca', '')
    filtro_pedigree = request.args.get('pedigree', '')

    # Busca IDs de pets que já receberam like ou pass
    ja_vistos = Curtida.query.filter_by(
        id_animal_de=animal.id
    ).with_entities(Curtida.id_animal_para).all()
    ids_ja_vistos = [c.id_animal_para for c in ja_vistos]

    # Busca pets da mesma cidade do tutor
    from app.models.usuario import Usuario
    tutores_mesma_cidade = Usuario.query.filter_by(
        id_cidade=current_user.id_cidade
    ).with_entities(Usuario.id).all()
    ids_tutores = [t.id for t in tutores_mesma_cidade]

    # Monta a query base
    query = Animal.query.filter(
        Animal.id_especie == animal.id_especie,
        Animal.id_usuario != current_user.id,
        Animal.id_usuario.in_(ids_tutores),
        Animal.id.notin_(ids_ja_vistos),
        Animal.id != animal.id
    )

    # Aplica filtros opcionais
    if filtro_genero:
        query = query.filter(Animal.genero == filtro_genero)
    if filtro_raca:
        query = query.filter(Animal.id_raca == filtro_raca)
    if filtro_pedigree:
        query = query.filter(Animal.pedigree == int(filtro_pedigree))

    candidatos = query.all()

    # Pega as raças da mesma espécie para o filtro
    racas = Raca.query.filter_by(id_especie=animal.id_especie).all()

    return render_template('buscar.html',
        animal=animal,
        candidatos=candidatos,
        racas=racas,
        filtro_genero=filtro_genero,
        filtro_raca=filtro_raca,
        filtro_pedigree=filtro_pedigree
    )
    
@pets.route('/swipe/<int:animal_id>/<int:alvo_id>/<direcao>')
@login_required
def swipe(animal_id, alvo_id, direcao):
    from app.models.curtida import Curtida
    from app.models.match import Match
    from app.models.notificacao import Notificacao
    from datetime import datetime

    animal = Animal.query.get_or_404(animal_id)
    alvo = Animal.query.get_or_404(alvo_id)

    if animal.id_usuario != current_user.id:
        flash('Você não tem permissão!', 'danger')
        return redirect(url_for('pets.meus_pets'))

    # Registra a curtida
    curtida = Curtida(
        id_animal_de=animal_id,
        id_animal_para=alvo_id,
        data=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    db.session.add(curtida)
    db.session.commit()

    # Se foi like, verifica match
    if direcao == 'like':
        like_de_volta = Curtida.query.filter_by(
            id_animal_de=alvo_id,
            id_animal_para=animal_id
        ).first()

        if like_de_volta:
            # Verifica se o match já existe
            match_existe = Match.query.filter(
                db.or_(
                    db.and_(Match.id_animal_1 == animal_id, Match.id_animal_2 == alvo_id),
                    db.and_(Match.id_animal_1 == alvo_id, Match.id_animal_2 == animal_id)
                )
            ).first()

            if not match_existe:
                # Cria o match
                novo_match = Match(
                    id_animal_1=animal_id,
                    id_animal_2=alvo_id,
                    data=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                db.session.add(novo_match)

                # Notifica os dois tutores
                notif_1 = Notificacao(
                    id_usuario=current_user.id,
                    mensagem=f'🎉 Match! {animal.nome} e {alvo.nome} deram match!',
                    data=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                notif_2 = Notificacao(
                    id_usuario=alvo.id_usuario,
                    mensagem=f'🎉 Match! {alvo.nome} e {animal.nome} deram match!',
                    data=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                db.session.add(notif_1)
                db.session.add(notif_2)
                db.session.commit()

                flash(f'💕 Match com {alvo.nome}!', 'success')
                return redirect(url_for('pets.buscar', animal_id=animal_id))

    return redirect(url_for('pets.buscar', animal_id=animal_id))