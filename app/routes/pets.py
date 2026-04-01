from flask import Blueprint

pets = Blueprint('pets', __name__)

@pets.route('/meus-pets')
def meus_pets():
    pass

@pets.route('/buscar/<int:animal_id>')
def buscar(animal_id):
    pass

@pets.route('/novo-pet')
def novo_pet():
    pass