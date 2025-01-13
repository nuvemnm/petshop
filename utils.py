import json

def save_user_to_session(page, user):
    # Transforma o objeto 'User' em um dicionário
    user_data = {
        "name": user.name,
        "email": user.email,
        "cpf": user.cpf,
        "address": user.address,
    }

    page.session.set("user", json.dumps(user_data))  