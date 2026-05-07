from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.anuncio import Anuncio
from datetime import datetime

admin = Blueprint('admin', __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.email != 'admin@petinder.com':
            flash('Acesso restrito!', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin')
@login_required
@admin_required
def painel():
    anuncios = Anuncio.query.order_by(Anuncio.id.desc()).all()
    return render_template('admin/painel.html', anuncios=anuncios)

@admin.route('/admin/novo-anuncio', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_anuncio():
    if request.method == 'POST':
        nome = request.form.get('nome_anunciante')
        imagem = request.form.get('imagem_url')
        link = request.form.get('link_url')

        anuncio = Anuncio(
            nome_anunciante=nome,
            imagem_url=imagem,
            link_url=link,
            ativo=1,
            criado_em=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(anuncio)
        db.session.commit()
        flash('Anúncio criado com sucesso!', 'success')
        return redirect(url_for('admin.painel'))

    return render_template('admin/novo_anuncio.html')

@admin.route('/admin/toggle-anuncio/<int:anuncio_id>')
@login_required
@admin_required
def toggle_anuncio(anuncio_id):
    anuncio = Anuncio.query.get_or_404(anuncio_id)
    if anuncio.esta_ativo():
        anuncio.desativar()
        flash('Anúncio desativado!', 'warning')
    else:
        anuncio.ativar()
        flash('Anúncio ativado!', 'success')
    db.session.commit()
    return redirect(url_for('admin.painel'))

@admin.route('/admin/excluir-anuncio/<int:anuncio_id>')
@login_required
@admin_required
def excluir_anuncio(anuncio_id):
    anuncio = Anuncio.query.get_or_404(anuncio_id)
    db.session.delete(anuncio)
    db.session.commit()
    flash('Anúncio excluído!', 'success')
    return redirect(url_for('admin.painel'))