import pandas as pd
from configs import USERS_TABLE_PATH
import os


class UserDatabase:
    def __init__(self):
        self.table_path = USERS_TABLE_PATH

    def is_name_taken(self, name):
        user_names = pd.read_csv(self.table_path,sep=";")["name"].values
        return (name in user_names)

    def get_current_id(self):
        max_id = max(pd.read_csv(USERS_TABLE_PATH,sep=";")["id_user"].values)
        return int(max_id)
    
    def insert_data(self, user):
        # Cria um dicionário com os dados do usuário
        data = {
            "id_user": [user.id_user],
            "name": [user.name],
            "password": [user.password],
            "email": [user.email],
            "cpf": [user.cpf],
            "address": [user.address]
        }

        try:
            # Converte o dicionário em um DataFrame
            new_user_df = pd.DataFrame(data)

            # Verifica se o arquivo CSV já existe
            if os.path.exists(USERS_TABLE_PATH):
                # Lê o arquivo existente
                existing_df = pd.read_csv(USERS_TABLE_PATH, delimiter=';', encoding='utf-8')

                # Concatena o novo usuário ao DataFrame existente
                updated_df = pd.concat([existing_df, new_user_df], ignore_index=True)
            else:
                # Caso o arquivo não exista, o novo DataFrame será usado diretamente
                updated_df = new_user_df

            # Salva o DataFrame atualizado no arquivo CSV
            updated_df.to_csv(USERS_TABLE_PATH, sep=';', index=False, encoding='utf-8')


            print(f"Linha inserida com sucesso no arquivo '{os.path.basename(USERS_TABLE_PATH)}'.")
        except Exception as e:
            print(f"Erro ao inserir a linha no CSV: {e}")