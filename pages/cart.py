from flet import *

from classes.product import Product

class Cart(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.cart = page.session.get("cart")

        self.title = Text("Carrinho",size=32)
        self.payment_button = ElevatedButton(text = 'Ir para pagamento', on_click = lambda _: self.page.go('/payment')) 
        self.back = ElevatedButton(text = 'Voltar', on_click = lambda _: self.page.go('/shop')) 
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


    def on_product_click(self, product):
        self.product = product
        self.modal_image.src = product.image
        self.modal_title.value = product.name
        self.modal_description.value = product.description
        self.modal.open = True
        self.page.update()


    def build(self):
        cards = []
        self.total_price = Text(self.cart.total_price,size=36)

        for index, row in self.cart.product_list.iterrows():
            product = Product(
                id_product=row["id_product"],
                name=row["name"],
                price=row["price"],
                quantity=row["quantity"],
                image=row["image"],
                description=row["description"]
            )
            
            card = GestureDetector(
                on_tap=lambda e, p=product: self.on_product_click(p),
                content=Card(
                    content=Container(
                        padding=10,
                        content=Row(
                            controls=[ 
                                Image(src=product.image, height=220, width=220, fit="COVER"),
                                Column(
                                    [
                                        Container(height=10),
                                        Text(product.name, size=26, weight="bold"),
                                        Text(f"R$ {product.price}", size=18),
                                        Text(f"Quantidade selecionada: {self.cart.get_quantity_in_cart(product.id_product)}", size=14),
                                    ],
                                    alignment="start",
                                    spacing=5,
                                ),
                            ],
                            alignment="start",
                            spacing=10,
                        ),
                    ),
                    width=240,
                    height=300,
                ),
            )
            cards.append(card)

        product_list = ListView(
            controls=cards,
            spacing=10,
            padding=10,
            height=600
        )

        return Container(
            content=Column(
                controls=[
                    self.title,
                    product_list,  # Container com os cards
                    self.total_price,
                    self.payment_button,
                    self.back
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )

    