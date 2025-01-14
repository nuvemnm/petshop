from flet import *
from elements import *
from src.product import Product
from ui.sucess_dialog import SucessDialog
from ui.modal import ItemDetailsModal
from ui.scrollable_list import Scrollable_list

class Cart(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.cart = self.page.session.get("cart")

        self.element = Elements()
        self.title = self.element.create_title("Carrinho") 
        self.payment_button = self.element.create_button("Finalizar Compra", lambda _: self.page.go('/payment'))  
        self.back = self.element.create_button("Voltar", lambda _: self.page.go('/shop')) 

        self.total_price_text = Text(size=18)
        self.lista = None

    def on_item_click(self, item):
        self.selected_item = item
        self.modal = ItemDetailsModal(
            item=item,
            on_close=self.close_modal,
            title_col_name="name",
            desc=f"R$ {item['price']},\nQuantidade selecionada: {item['quantity']}",
            buttons_list=self.modal_buttons
        ).build()

        self.page.dialog = self.modal
        self.page.dialog.open = True
        self.page.update()

    def close_modal(self):
        self.selected_item = None
        self.page.dialog.open = False
        self.page.update()

    def refresh_cart_data(self):
        self.cart = self.page.session.get("cart")
        self.total_price_text = Text(f"Total: R$ {self.cart.get_total_price():.2f}", size=18, weight="bold")
    
    def update_list(self):
        # Reconstrua a lista com os dados atualizados
        self.lista = Scrollable_list(
            dataframe=self.cart.product_list,
            title_col_name="name",
            desc_col_names={'price': 'R$', 'quantity': 'Quantidade disponível'},
            on_item_click=self.on_item_click
        )

        # Atualize os controles da página
        self.controls.clear()
        self.controls.append(
            Container(
                content=Column(
                    controls=[
                        self.title,
                        self.lista.build(),  # Construa a lista atualizada
                        self.total_price_text,
                        self.payment_button,
                        self.back
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                alignment=alignment.center,
            )
        )
        self.update()

    def remove_from_cart(self,selected_item):
        product = selected_item.copy()
        if self.cart.get_quantity_in_cart(product["id_product"]) > 0:
            self.cart.remove_product(product)

            success_dialog = SucessDialog("Item removido do carrinho com sucesso!",product["name"],self.page)
            success_dialog.show()
            self.refresh_cart_data()
            self.update_list()
        else:
            dlg = AlertDialog(
                title=Text("Não foi possível remover o item do carrinho"),
            )
            self.page.open(dlg)
        print(self.cart.product_list.shape)

    def go_payment(self):
        payment_info = {"price":self.cart.get_total_price(),"products":self.cart.product_list,"origin_page":"cart"}
        self.page.session.set("payment_info",payment_info)
        self.page.go('/payment')

    def build(self):
        self.lista = Scrollable_list(
            dataframe=self.cart.product_list,
            title_col_name="name",
            desc_col_names={'price': 'R$', 'quantity': 'Quantidade disponível'},
            on_item_click=self.on_item_click
        )

        self.total_price_text = Text(f"Total: R$ {self.cart.get_total_price():.2f}", size=18, weight="bold")

        self.modal_buttons = [
            ElevatedButton(
                text="Remover do carrinho",
                on_click=lambda e, p=None: self.remove_from_cart(self.selected_item),
                expand=True,
                height=100,
                style=ButtonStyle(
                    color="white",
                    bgcolor="red",
                    shape=RoundedRectangleBorder(20)
                ),
                icon=icons.ADD,
            ),
        ]

        return Container(
            content=Column(
                controls=[
                    self.title,
                    self.lista.build(),  # Construa a lista inicial
                    self.total_price_text,
                    self.payment_button,
                    self.back
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
            alignment=alignment.center,
        )
        