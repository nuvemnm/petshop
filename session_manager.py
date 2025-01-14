

import pandas as pd
from src.user import User
from configs import PETS_TABLE_PATH

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

def load_user_from_session(page):
    user_data = page.session.get("user")
    if user_data is None:
        return None
    return User(user_data["id_user"],user_data['name'], user_data['password'], user_data['email'], user_data['cpf'], user_data['address'])