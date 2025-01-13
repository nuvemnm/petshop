from flet import *
import csv
from classes.product import Product  # Importando a classe Product

class Pets(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.products = []
        
        self.title = Text("Meus Pets")
        self.cart = ElevatedButton(text='Carrinho', on_click=lambda _: self.page.go('/cart')) 
        self.back = ElevatedButton(text='Voltar', on_click=lambda _: self.page.go('/menu'))

    def collect_products(self):
        try:
            self.products.clear()  # Limpa a lista antes de recarregar os produtos
            with open("csv/products.csv", mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for line in reader:
                    if len(line) >= 3:
                        name, price, quantity, image = line
                        self.products.append(Product(name, price, quantity, image))
            return True
        except FileNotFoundError:
            print(f"Erro: Arquivo 'products.csv' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False

    def build(self):
        if not self.collect_products():
            return Text("Erro ao carregar produtos.")

        cards = []
        for product in self.products:
            card = Card(
                content=Container(
                    padding=10,
                    content=Column(
                        [
                            Image(src="images/products/biscoito.jpg", height=100, width=100, fit="cover"),
                            Text(product.name, size=18, weight="bold"),
                            Text(product.price, size=16),
                            Text(f"Quantidade: {product.quantity}", size=14),
                        ],
                        alignment="center",
                        spacing=5,
                    ),
                ),
                width=200,
                height=250,
            )
            cards.append(card)

        return Container(
            content=Column(
                controls=[
                    self.title,
                    *cards,  # Adiciona todos os cards
                    self.cart,
                    self.back,
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )
