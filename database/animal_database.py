import pandas as pd
from configs import PETS_TABLE_PATH
import os

class AnimalDatabase:
    def __init__(self):
        self.pets_table_path = PETS_TABLE_PATH

    def get_pet_list_by_user_id(self,user_id):
        pet_list = pd.read_csv(PETS_TABLE_PATH,sep=";")
        user_pet_df = pet_list[pet_list["id_user"] == user_id]
        return user_pet_df


    def insert_data(self, animal):
        # Criação do DataFrame com os dados do animal
        new_data = pd.DataFrame([{
            "id_pet": animal.id_pet,
            "id_user": animal.id_user,
            "specie": animal.specie,
            "name": animal.name,
            "sex": animal.sex,
            "castrated": animal.castrated,
            "race": animal.race,
            "age": animal.age,
            "weight": animal.weight,
            "image": animal.image
        }])

        try:
            # Verifica se o arquivo já existe
            if os.path.exists(self.pets_table_path):
                # Lê o arquivo existente e adiciona os novos dados
                existing_data = pd.read_csv(self.pets_table_path, sep=";")
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            else:
                # Se o arquivo não existe, cria com os novos dados
                updated_data = new_data

            # Salva os dados no arquivo CSV
            updated_data.to_csv(self.pets_table_path, index=False, encoding='utf-8',sep=";")
            print(f"Cadastro realizado com sucesso: {new_data.iloc[0].to_dict()}")
            return True
        
        except Exception as ex:
            print(f"Erro ao inserir os dados: {ex}")
            return False

    def get_current_id(self):
        try:
            max_id = max(pd.read_csv(PETS_TABLE_PATH, sep=";")["id_pet"].values)
            return max_id or 0
        except Exception as e:
            print(f"Erro ao obter ID atual: {e}")
            return 0
