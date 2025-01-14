import json
from configs import *

import pandas as pd
from classes.user import User
from classes.animals import Animal

def save_user_to_session(page, user):
    # Transforma o objeto 'User' em um dicionário
    user_data = {
        "id_user" : user.id_user,
        "name": user.name,
        "password":user.password,
        "email": user.email,
        "cpf": user.cpf,
        "address": user.address,
    }

    page.session.set("user", user_data)
    save_user_pets_to_session(page,user_data["id_user"])

def save_user_pets_to_session(page, user_id):
    user_pet_list = get_pet_list_with_user_id(user_id)
    page.session.set("pet_list", user_pet_list)

def load_pet_list_from_session(page):
    pet_list = page.session.get("pet_list") 
    return pet_list

def get_pet_list_with_user_id(user_id):
    pet_list = pd.read_csv(PETS_TABLE_PATH,sep=";")
    user_pet_df = pet_list[pet_list["id_user"] == user_id]
    return user_pet_df

def load_user_from_session(page):
    user_data = page.session.get("user")
    if user_data is None:
        return None
    return User(user_data["id_user"],user_data['name'], user_data['password'], user_data['email'], user_data['cpf'], user_data['address'])

