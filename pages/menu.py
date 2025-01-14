from flet import *
import csv
import pandas as pd
from configs import *
from database.animal_database import AnimalDatabase
from src.user import User
from ui.elements import *
from session_manager import load_user_from_session

class Menu(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.animal_database = AnimalDatabase()
        self.element = Elements()
        self.padding = Container(height=40)
        self.user = load_user_from_session(self.page)
        self.user_name = Text(f"Olá,")
        self.has_pet = False

        if(self.user):
            self.user_name = Text(f"Olá, {self.user.name}")
        
        self.title = self.element.create_title("Menu Principal")
        self.shop = self.element.create_button("Loja", lambda _: self.page.go('/shop'))

        self.myPets = self.element.create_button("Meus Pets", self.go_pets)
        self.my_purchases = self.element.create_button("Minhas Compras",lambda _: self.page.go('/purchases'))
        self.out = self.element.create_button("Sair", self.close_app)

    def close_app(self, e):
        self.page.window.close()

    def build(self):
        self.verify_pet()
        return Container(
            content=Column(
                controls=[
                    self.user_name,
                    self.title,
                    self.padding,
                    self.shop,
                    self.myPets,
                    self.my_purchases,
                    self.out         
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  
            ),
            alignment=alignment.center,  
        )

    def go_pets(self,e):
        if self.has_pet:
            self.page.go('/pets')
        else:
            self.page.go('/pet_register')

    
    def verify_pet(self):
        try:
            if not self.animal_database.get_pet_list_by_user_id(self.user.id_user).empty:
                self.has_pet = True
            else:
                self.has_pet = False

            return False  
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo}' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False
