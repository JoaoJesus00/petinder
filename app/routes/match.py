@app.route('/curtir/<int:id_animal_para>', methods=['POST'])
def curtir(id_animal_para):
    if 'id_usuario' not in session:
        return redirect(url_for('login'))

    con = conectar()
    cur = con.cursor()
    try:
        # Pega o primeiro animal do usuário logado
        cur.execute('SELECT id FROM animal WHERE id_usuario = ?', (session['id_usuario'],))
        meu_animal = cur.fetchone() #seleciona apenas um, vai até encontrar

        if not meu_animal: #se não existir
            flash('Você precisa cadastrar um animal primeiro!', 'danger')
            return redirect(url_for('index'))

        # Registra a curtida
        cur.execute('''
            INSERT INTO curtida (id_animal_de, id_animal_para, data)
            VALUES (?, ?, datetime('now'))
        ''', (meu_animal['id'], id_animal_para))#joga na tabela de curtida, o id/ chave estrangeira de quem é/ data
        con.commit()#salva

        # Verifica se o outro animal também curtiu (match!)
        cur.execute('''
            SELECT id FROM curtida
            WHERE id_animal_de = ? AND id_animal_para = ?
        ''', (id_animal_para, meu_animal['id'])) #busca id e chave estrangeira de para
        match = cur.fetchone() #busca só um

        if match: #Se o outro jpá tinha curtido o primeiro antes
                    # select buscou na tabela curtida se já existe
                    # id_animal_de = o outro, id_animal_para = eu
                    # se fetchone achou alguma coisa, é porque o outro já curtiu
            cur.execute('''
                INSERT INTO match (id_animal_1, id_animal_2, data)
                VALUES (?, ?, datetime('now'))
            ''', (meu_animal['id'], id_animal_para)) #joga na tabela match
            con.commit()#salva
            flash('🎉 É um match!', 'success') #duas curtidas
        else:
            flash('Curtida enviada!', 'success') #msg da primeira curtida

    finally:
        con.close()

    return redirect(url_for('explorar')) #volta pra página de explorar;