from flet import *
import pandas as pd
import csv
from configs import *
from classes.product import Product
from dialogs.sucess_dialog import SucessDialog  
from cart import Shopping_Cart
from modal import ItemDetailsModal
from scrollable_list import Scrollable_list

class Shop(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.product_list = []
        self.selected_item = None

        self.title = Text("Loja",size=32)

        if not self.page.session.get("cart"):
            page.session.set("cart", Shopping_Cart())

        self.cart = self.page.session.get("cart")

        self.cart_button = ElevatedButton(text="Carrinho", on_click=lambda _: self.page.go('/cart')
        )
        self.back = ElevatedButton(text='Voltar', on_click=lambda _: self.page.go('/menu'))

    def on_item_click(self, item):
        self.selected_item = item
        self.modal = ItemDetailsModal(
            item=item,
            on_close=self.close_modal,
            title_col_name="name",
            desc=f"R$ {item['price']},\nQuantidade disponível: {item['quantity']}",
            buttons_list=self.modal_buttons
        ).build()

        self.page.dialog = self.modal
        self.page.dialog.open = True
        self.page.update()

    def close_modal(self):
        self.selected_item = None
        self.page.dialog.open = False
        self.page.update()

    def load_products(self):
        try:
            products_df = pd.read_csv(PRODUCTS_TABLE_PATH,sep=";")
            return products_df
        except FileNotFoundError:
            print(f"Erro: Arquivo 'products.csv' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False



    def add_to_cart(self,selected_item):
        product = selected_item.copy()
        
        if self.cart.get_quantity_in_cart(product['id_product']) < product['quantity']:
            self.cart.add_product(product)
            
            success_dialog = SucessDialog("Item adicionado ao carrinho com sucesso!",product["name"],self.page)
            success_dialog.show()

        else:
            dlg = AlertDialog(
                title=Text("Não foi possível adicionar o item ao carrinho"),
                content=Text("Estamos sem estoque."),
            )
            self.page.open(dlg)

    def build(self):
        products_df = self.load_products()

        self.modal_buttons = [
                    ElevatedButton(
                        text="Adicionar ao Carrinho",
                        on_click=lambda e, p=None: self.add_to_cart(self.selected_item),
                        expand=True,
                        height=100,
                        style=ButtonStyle(
                            color="white",
                            bgcolor="green",
                            shape=RoundedRectangleBorder(20)
                        ),
                        icon=icons.ADD,
                    ),
        ]
        
        lista = Scrollable_list(
            dataframe=products_df,
            title_col_name="name",
            desc_col_names={'price':'R$','quantity':'Quantidade disponível'},
            on_item_click=self.on_item_click
        )

        return Container(
            content=Column(
                controls=[
                    self.title,
                    lista.build(),  # Container com os cards
                    Row(
                        controls=[
                            self.cart_button,
                            self.back,
                        ],
                        alignment="center",  
                        spacing=20, 
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )

