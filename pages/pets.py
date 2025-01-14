from flet import *
import pandas as pd
import csv
from configs import *
from utils import * 
from classes.animals import Animal  # Importando a classe Product

class Pets(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.title = Text("Meus Pets",size=32)

        self.pets = load_pet_list_from_session(self.page)

        self.new_pet = ElevatedButton(text='Cadastrar Novo Pet', on_click=lambda _: self.page.go('/pet_register'), height=30)
        self.back = ElevatedButton(text='Voltar', on_click=lambda _: self.page.go('/menu'), height=30)
        self.pets_list = load_pet_list_from_session(self.page)
        self.modal_image = Image(width=600, height=400, fit="contain")
        self.modal_title = Text(size=22, weight="bold")
        self.modal_age = Text(size=16)

        self.modal = AlertDialog(
            modal=True,
            open=False,
            content=Container(
                padding=20,
                content=Column(
                    [
                        self.modal_image,
                        self.modal_title,
                        self.modal_age
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
            ),
            actions=[
                Row(
                    controls=[
                        ElevatedButton(
                            text="Banho e Tosa",
                            on_click=lambda e: self.page.go('/wash'),
                            expand=True,
                            height=70,
                        ),
                        ElevatedButton(
                            text="Veterinaria",
                            on_click=lambda e: self.page.go('/veterinaria'),
                            expand=True,
                            height=70,
                        ),
                        
                    ],
                ),
                Container(height=20),  # Remove o espaçamento entre os botões
                Row(
                    controls = [
                        ElevatedButton(
                            text="Voltar",
                            on_click=lambda e: self.hide_modal(e),
                            expand=True,
                            height=50,
                        ),
                    ],
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
        self.modal_age.value = ""


    def on_pet_click(self, pet):
        self.modal_image.src = pet["image"]
        self.modal_title.value = pet["name"]
        self.modal_age.value = pet["age"]
        self.modal.open = True
        self.page.update()


    def build(self):
        
        cards = []
        for _, pet in self.pets.iterrows():

            card = GestureDetector(
                on_tap=lambda e, p = pet: self.on_pet_click(p),
                content=Card(
                    content=Container(
                        padding=10,
                        content=Row(
                            controls=[
                                # Imagem do produto (esquerda)
                                Image(src=pet["image"], height=180, width=180, fit="FIT_HEIGHT"),
                                
                                # Informações do produto (direita)
                                Column(
                                    [
                                        Text(pet["name"], size=26, weight="bold"),
                                        Text(f"Idade {pet['age']}", size=18),
                                        Text(f"Raça: {pet['race']}", size=14),
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
                    height=210,
                ),  
            )
            cards.append(card)
        self.page.dialog = self.modal

        pet_list = ListView(
            controls=cards,
            spacing=10,
            padding=10,
            height=380
        )

        return Container(
            content=Column(
                controls=[
                    self.title,
                    Container(height=20),
                    pet_list,  # Container com os cards
                    self.new_pet,
                    self.back,
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )

