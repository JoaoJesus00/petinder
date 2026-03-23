# Transforma a pasta em módulo, e centraliza os modelos para facilitar a importação

from app.models.usuario import Usuario
from app.models.animal import Animal
from app.models.match import Match
from app.models.notificacao import Notificacao
from app.models.anuncio import Anuncio
from app.models.especie import Especie

# Importa todas as classes dos modelos para facilitar a importação para outros lugares dentro do projeto