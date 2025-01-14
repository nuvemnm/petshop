import pandas as pd
from configs import PURCHASES_TABLE_PATH
from src.user import User


class PurchasesDatabase:
    def __init__(self):
        self.table_path = PURCHASES_TABLE_PATH


    def get_current_purchase_id(self):
        df = pd.read_csv(self.table_path, sep=";")
        
        if df.empty:
            return 0
        
        max_id = df["id_purchase"].max() 
        return int(max_id) if pd.notna(max_id) else 0


    def insert_purchase(self, user : User, type : str, product : pd.DataFrame):
        if type == "cart":
            purchases_df = pd.read_csv(self.table_path, sep=";")

            new_rows = []

            # Adiciona o produto fornecido
            new_rows.append({
                "id_purchase": self.get_current_purchase_id() + 1,
                "id_product": product["id_product"],
                "id_user": user.id_user,
                "name": product["name"],
                "price": product["price"],
                "date": pd.to_datetime("today").strftime("%Y-%m-%d"),  # Data de compra
                "description": product["description"],
                "image": product["image"],
                "status": "Preparando pedido"
            })

            # Criar um DataFrame para a nova linha
            new_df = pd.DataFrame(new_rows)

            # Adicionar a nova linha ao DataFrame existente
            purchases_df = pd.concat([purchases_df, new_df], ignore_index=True)

            # Salvar o DataFrame atualizado no CSV, preservando as informações existentes
            purchases_df.to_csv(self.table_path, sep=";", index=False)
        
        elif type == "wash":
            purchases_df = pd.read_csv(self.table_path, sep=";")
            new_rows = []
            new_rows.append({
                "id_purchase":self.get_current_purchase_id()+1,
                "id_service": product[0],
                "id_user":user.id_user,
                "name": product[1],
                "price": product[2],
                "date": pd.to_datetime("today").strftime("%Y-%m-%d"),  # Data de compra
                "status": "Aguardando data"
            })
            # Criar um DataFrame para as novas linhas
            new_df = pd.DataFrame(new_rows)

            # Adicionar as novas linhas ao DataFrame existente
            purchases_df = pd.concat([purchases_df, new_df], ignore_index=True)

            # Salvar o DataFrame atualizado no CSV, preservando as informações existentes
            purchases_df.to_csv(self.table_path, sep=";", index=False)

