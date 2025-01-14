from flet import *
import pandas as pd
import csv
from configs import *
from classes.product import Product
from dialogs.sucess_dialog import SucessDialog  
from cart import Shopping_Cart

class Shop(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.product_list = []
        self.title = Text("Loja",size=32)
        if not self.page.session.get("cart"):
            page.session.set("cart", Shopping_Cart())

        self.cart = self.page.session.get("cart")

        self.cart_button = ElevatedButton(text="Carrinho", on_click=lambda _: self.page.go('/cart'))
        self.back = ElevatedButton(text='Voltar', on_click=lambda _: self.page.go('/menu'))
        
        self.modal_image = Image(width=600, height=400, fit="contain")
        self.modal_title = Text(size=22, weight="bold")
        self.modal_description = Text(size=18)

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
                        on_click=lambda e, p=None: self.add_to_cart(p),
                        expand=True,
                        height=100,
                        style=ButtonStyle(
                            color="white",
                            bgcolor="green",
                            shape=RoundedRectangleBorder(20)
                        ),
                        icon=icons.ADD,
                    ),
                    ElevatedButton(
                        text="Voltar",
                        on_click=lambda e: self.hide_modal(e),
                        expand=True,
                        height=100,
                        style=ButtonStyle(
                            color="white",
                            bgcolor="red",
                            shape=RoundedRectangleBorder(20)
                        ),
                    ),
                ],
                spacing=10,
            ),
            ],
        )

    def add_to_cart(self, product):
        if self.cart.get_quantity_in_cart(product.id_product) < product.quantity:
            self.cart.add_product(product)
            
            success_dialog = SucessDialog("Item adicionado ao carrinho com sucesso!",product.name,self.page)
            success_dialog.show()

        else:
            dlg = AlertDialog(
                title=Text("Não foi possível adicionar o item ao carrinho"),
                content=Text("Estamos sem estoque."),
            )
            self.page.open(dlg)


    def hide_modal(self,e):
        # Remove o modal da tela:
        self.modal.open = False
        self.page.update()

        # Remove os dados do modal:
        self.modal_image.src = ""
        self.modal_title.value = ""
        self.modal_description.value = ""


    def on_product_click(self, product):
        self.product = product
        self.modal_image.src = product.image
        self.modal_title.value = product.name
        self.modal_description.value = product.description
        self.modal.open = True
        self.modal.actions[0].controls[0].on_click = lambda e: self.add_to_cart(product)
        self.page.update()


    def load_products(self):
        try:
            products = pd.read_csv(PRODUCTS_TABLE_PATH,sep=";")
            self.product_list = [
                Product(
                    id_product=row["id_product"],
                    name=row["name"],
                    price=row["price"],
                    quantity=row["quantity"],
                    image=row["image"],
                    description=row["description"],
                )
                for _, row in products.iterrows()
            ]
        
        except FileNotFoundError:
            print(f"Erro: Arquivo 'products.csv' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False

    def build(self):
        self.products = self.load_products()
        if self.products:
            return Text("Erro ao carregar produtos.")
        
        cards = []
        for product in self.product_list:
            card = GestureDetector(
                on_tap=lambda e, p=product: self.on_product_click(p),
                content=Card(
                    content=Container(
                        padding=10,
                        content=Row(
                            controls=[ 
                                # Imagem do produto (esquerda)
                                Image(src=product.image, height=220, width=220, fit="COVER"),
                                
                                # Informações do produto (direita)
                                Column(
                                    [
                                        Container(height=10),
                                        Text(product.name, size=26, weight="bold"),
                                        Text(f"R$ {product.price}", size=18),
                                        Text(f"Quantidade disponível: {product.quantity}", size=14),
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
            height=580
        )

        return Container(
            content=Column(
                controls=[
                    self.title,
                    product_list,  # Container com os cards
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

