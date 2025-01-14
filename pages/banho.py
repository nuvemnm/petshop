from flet import *
import pandas as pd

from configs import SERVICES_TABLE_PATH
from list import Scrollable_list
from modal import ItemDetailsModal

class Banho(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.title = Text("Banho e Tosa")
        
        self.payment = ElevatedButton(text = 'Finalizar Pagamento', on_click = lambda _: self.page.go('/pets')) 
        self.back = ElevatedButton(text = 'Voltar', on_click = lambda _: self.page.go('/pets')) 

        self.selected_item = None
        self.modal = None

    def on_item_click(self, item):
        self.selected_item = item
        self.modal = ItemDetailsModal(
            item=item,
            on_close=self.close_modal,
            title_col_name="name",
            desc=f"Preço: R${item['price']}",
        ).build()

        self.page.dialog = self.modal
        self.page.dialog.open = True
        self.page.update()



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

    
