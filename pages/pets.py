from flet import *
import pandas as pd
import csv
from configs import *
from database.animal_database import AnimalDatabase
from ui.elements import * 
from ui.modal import ItemDetailsModal
from ui.scrollable_list import Scrollable_list
from session_manager import * 
from src.animals import Animal  # Importando a classe Product

class Pets(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.element = Elements()

        self.animal_database = AnimalDatabase()
        self.title = self.element.create_title("Meus Pets")
        self.new_pet = self.element.create_button("Cadastrar Novo Pet", lambda _: self.page.go('/pet_register'))
        self.back = self.element.create_button("Voltar", lambda _: self.page.go('/menu'))

        self.user = load_user_from_session(self.page)



    def on_item_click(self, item):
        self.selected_item = item
        self.modal = ItemDetailsModal(
            item=item,
            on_close=self.close_modal,
            title_col_name="name",
            desc=f"Espécie: {item['specie']},\n Peso: {item['weight']}",
            buttons_list=self.modal_buttons
        ).build()

        self.page.dialog = self.modal
        self.page.dialog.open = True
        self.page.update()

    def close_modal(self):
        self.selected_item = None
        self.page.dialog.open = False
        self.page.update()

    def get_pets(self):
        return self.animal_database.get_pet_list_by_user_id(self.user.id_user)

    def build(self):
        pets_list = self.get_pets()
        lista = Scrollable_list(
            dataframe=pets_list,
            title_col_name="name",
            desc_col_names={'specie':'Espécie','race':'Raça'},
            on_item_click=self.on_item_click
        )

        self.modal_buttons = [
            ElevatedButton("Banho e Tosa", on_click=lambda _: self.page.go('/wash'),height=50),
        ]

        return Container(
            content=Column(
                controls=[
                    self.title,
                    Container(height=20),
                    lista.build(),  # Container com os cards
                    self.new_pet,
                    self.back,
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )

