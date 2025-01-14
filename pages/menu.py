from flet import *
import csv
import pandas as pd
from configs import *
from classes.user import User
from elements import *
from utils import load_user_from_session,load_pet_list_from_session

class Menu(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.element = Elements()

        self.user = load_user_from_session(self.page)
        self.user_name = Text(f"Olá,")

        self.pet_list = load_pet_list_from_session(self.page)

        if(self.user):
            self.user_name = Text(f"Olá, {self.user.name}")
        
        self.title = self.element.create_title("Menu Principal")
        self.shop = self.element.create_button("Loja", lambda _: self.page.go('/shop'))
        self.myPets = self.element.create_button("Meus Pets", self.verify_pet)
        self.my_purchases = self.element.create_button("Minhas Compras",lambda _: self.page.go('/purchases'))
        self.out = self.element.create_button("Sair", self.close_app)

    def close_app(self, e):
        self.page.window.close()

    def build(self):
        print()
        return Container(
            content=Column(
                controls=[
                    self.user_name,
                    self.title,
                    self.shop,
                    self.myPets,
                    self.my_purchases,
                    self.out         
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  
            ),
            alignment=alignment.center,  
        )

    
    def verify_pet(self,e):
       
        try:
            if self.pet_list.empty:
                self.page.go('/pet_register')
            else:
                print("nao vazio")
                self.page.go('/pets')

            return False  
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo}' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False
