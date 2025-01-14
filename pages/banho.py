from flet import *
import pandas as pd
from elements import *
from configs import SERVICES_TABLE_PATH
from ui.modal import ItemDetailsModal
from ui.scrollable_list import Scrollable_list

class Banho(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.element = Elements()

        self.title = self.element.create_title("Banho e Tosa")
         
        self.payment = self.element.create_button("Finalizar Pagamento", lambda _: self.page.go('/payment')) 
        self.back = self.element.create_button("Voltar", lambda _: self.page.go('/pets'))


        self.selected_item = None
        self.modal = None

    def on_item_click(self, item):
        self.selected_item = item
        self.go_payment()

    def go_payment(self):
        payment_info = {"price":self.selected_item["price"],"products":self.selected_item,"origin_page":"wash"}
        self.page.session.set("payment_info",payment_info)
        self.page.go('/payment')


    def close_modal(self):
        self.selected_item = None
        self.page.dialog.open = False
        self.page.update()



    def get_services(self):
        try:
            return pd.read_csv(SERVICES_TABLE_PATH,sep=";")
        except Exception as ex:
            print("Não foi possível obter os dados de serviços,",ex)

    def build(self):
        services_df = self.get_services()


        lista = Scrollable_list(
            dataframe=services_df,
            title_col_name="name",
            desc_col_names={'price':'Preço do serviço'},
            on_item_click=self.on_item_click
        )

        return Container(
            content=Column(
                controls=[
                    self.title,
                    lista.build(),
                    self.payment,
                    self.back
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )

    
