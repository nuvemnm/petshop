from flet import *
from utils import *
from pages.cart import *
from elements import *
import pandas as pd

class Purchases(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.title = Text("Minhas compras")
        user = self.page.session.get("user")
        if user:
            self.user = user
        self.back = ElevatedButton(text='Voltar', on_click=lambda _: self.page.go('/menu'))

    def get_user_purchases(self):
        purchases = pd.read_csv(PURCHASES_TABLE_PATH,sep=";")
        user_purchases = purchases[purchases["id_user"] == self.user["id_user"]]
        return user_purchases
    
    def on_item_click(self):
        pass

    def build(self):

        purchases_df = self.get_user_purchases()

        lista = Scrollable_list(
            dataframe=purchases_df,
            title_col_name="name",
            desc_col_names={'date':'Data do pedido','status':"Status atual"},
            on_item_click=self.on_item_click
        )

        return Container(
            content=Column(
                controls=[
                    self.title,
                    lista.build(),  # Container com os cards
                    Row(
                        controls=[
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
