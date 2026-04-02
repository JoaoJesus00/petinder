# Esse arquivo é o que inicia o sistema, é o único a ser executado no terminal para colocar o site no ar
# Chama a função criada em __init__.py
from app import create_app # Essa função monta o site completo

app = create_app() # Chamando a função do __init__ e guardando na variável "app"
if __name__ == '__main__':
    # Só liga o servidor se rodar esse arquivo diretamente, pois o arquivo vai ser importado por outros
    app.run(debug=True) # Aqui o Flask liga o servidor local na porta 5000
    # O debug serve para que se você altere qualquer arquivo o servidor reinicia sozinho, e se der erro ele mostra uma mensagem no navegador