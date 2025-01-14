import pandas as pd
from configs import PRODUCTS_TABLE_PATH


class ProductDatabase:
    def __init__(self):
        self.table_path = PRODUCTS_TABLE_PATH


    def get_all_products(self):
        try:
            products_df = pd.read_csv(self.table_path,sep=";")
            return products_df
        except FileNotFoundError:
            print(f"Erro: Arquivo 'products.csv' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False


    def decrease_item(self, product):
        print(f"==============\n{product}\n============")
        # Lê o arquivo CSV para carregar os produtos existentes
        products_df = pd.read_csv(self.table_path, sep=";")

        if not products_df.empty:
            # Localiza o índice do produto no DataFrame com base no ID do produto
            product_index = products_df[products_df["id_product"] == product.id_product].index

            if len(product_index) > 0:
                # Reduzir a quantidade do produto encontrado
                products_df.at[product_index[0], "quantity"] -= 1

                # Garante que a quantidade não seja negativa
                if products_df.at[product_index[0], "quantity"] < 0:
                    products_df.at[product_index[0], "quantity"] = 0

                # Salvar as alterações de volta no arquivo CSV
                products_df.to_csv(self.table_path, sep=";", index=False)
                print(f"Quantidade do produto com ID {product.id_product} atualizada com sucesso.")
            else:
                print(f"Produto com ID {product.id_product} não encontrado no inventário.")
        else:
            print("Não há produtos no inventário.")