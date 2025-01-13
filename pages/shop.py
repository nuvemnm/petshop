from flet import *
import pandas as pd
import csv
from configs import *
from classes.product import Product  # Importando a classe Product

class Shop(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.products = pd.DataFrame()
        self.title = Text("Loja",size=32)

        self.cart = ElevatedButton(text='Carrinho', on_click=lambda _: self.page.go('/cart')) 
        self.back = ElevatedButton(text='Voltar', on_click=lambda _: self.page.go('/menu'))
        
        self.modal_image = Image(width=600, height=400, fit="contain")
        self.modal_title = Text(size=22, weight="bold")
        self.modal_description = Text(size=16)

        self.modal = AlertDialog(
            modal=True,
            open=False,
            content=Container(
                padding=20,
                content=Column(
                    [
                        self.modal_image,
                        self.modal_title,
                        self.modal_description
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
            ),
            actions=[
                Row(
                    controls=[
                        ElevatedButton(
                            text="Adicionar ao Carrinho",
                            on_click=lambda e: self.add_to_cart(e),
                            expand=True,
                            height=100,
                        ),
                        ElevatedButton(
                            text="Voltar",
                            on_click=lambda e: self.hide_modal(e),
                            expand=True,
                            height=100,
                        ),
                    ],
                    spacing=0,  # Remove o espaçamento entre os botões
                ),
            ],
        )

    def hide_modal(self,e):
        # Remove o modal da tela:
        self.modal.open = False
        self.page.update()

        # Remove os dados do modal:
        self.modal_image.src = ""
        self.modal_title.value = ""
        self.modal_description.value = ""


    def on_product_click(self, product):
        self.modal_image.src = product["image"]
        self.modal_title.value = product["name"]
        self.modal_description.value = product["description"]
        self.modal.open = True
        self.page.update()


    def collect_products(self):
        try:
            self.products = pd.read_csv(PRODUCTS_TABLE_PATH,sep=";")
            return self.products
        except FileNotFoundError:
            print(f"Erro: Arquivo 'products.csv' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False

    def build(self):
        self.products = self.collect_products()
        if self.products.empty:
            return Text("Erro ao carregar produtos.")
        
        cards = []
        for _, product in self.products.iterrows():

            card = GestureDetector(
                on_tap=lambda e, p=product: self.on_product_click(p),
                content=Card(
                    content=Container(
                        padding=10,
                        content=Row(
                            controls=[
                                # Imagem do produto (esquerda)
                                Image(src=product["image"], height=180, width=180, fit="FIT_HEIGHT"),
                                
                                # Informações do produto (direita)
                                Column(
                                    [
                                        Text(product["name"], size=26, weight="bold"),
                                        Text(f"R$ {product['price']}", size=18),
                                        Text(f"Quantidade disponível: {product['quantity']}", size=14),
                                    ],
                                    alignment="start",  # Alinha à esquerda
                                    spacing=5,
                                ),
                            ],
                            alignment="start",  # Alinha os itens na parte superior
                            spacing=10,  # Espaço entre a imagem e as informações
                        ),
                    ),

                    width=240,
                    height=300,
                ),  
            )
            cards.append(card)
        self.page.dialog = self.modal

        product_list = ListView(
            controls=cards,
            spacing=10,
            padding=10,
            height=800
        )

        return Container(
            content=Column(
                controls=[
                    self.title,
                    product_list,  # Container com os cards
                    Row(
                        controls=[
                            self.cart,
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

