
from classes.product import Product
import pandas as pd

class Shopping_Cart:
    def __init__(self):
        self.product_list = pd.DataFrame(columns=["id_product", "name", "price", "quantity", "image", "description"])
        self.total_price = 0
        self.len = 0

    def add_product(self, product : Product):
        if product.id_product in self.product_list["id_product"].values:
            self.product_list.loc[self.product_list["id_product"] == product.id_product, "quantity"] += 1
        else:
            new_product = pd.DataFrame([[product.id_product, product.name, product.price, 1, product.image, product.description]],
                                       columns=["id_product", "name", "price", "quantity", "image", "description"])
            self.product_list = pd.concat([self.product_list, new_product], ignore_index=True)

        self.len += 1
        self.total_price += product.price

    def get_quantity_in_cart(self, id_product):
        # Retorna a quantidade do produto no carrinho
        quantity = self.product_list.loc[self.product_list["id_product"] == id_product, "quantity"]
        if not quantity.empty:
            return quantity.iloc[0]  # Retorna o valor da quantidade
        return 0  # Se o produto não estiver no carrinho

    def get_total_price(self):
        # Retorna o preço total (para facilitar)
        return self.total_price

    def get_cart(self):
        # Retorna o carrinho (DataFrame) completo para visualização ou manipulação
        return self.product_list

