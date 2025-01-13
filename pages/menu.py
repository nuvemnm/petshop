from flet import *
import csv
import pandas as pd
from configs import *
from classes.user import User
from utils import load_user_from_session

class Menu(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.user = load_user_from_session(self.page)
        self.user_name = Text(f"Olá,")

        if(self.user):
            self.user_name = Text(f"Olá, {self.user.name}")
        
        self.title = Text("Menu Principal")
        self.shop = ElevatedButton(text = 'Loja', on_click = lambda _: self.page.go('/shop'))  
        self.myPets = ElevatedButton(text = 'Meus Pets', on_click = self.verify_pet)  
        self.out = ElevatedButton(text='Sair', on_click=self.close_app)    

    def close_app(self, e):
        self.page.window.close()

    def build(self):
        
        return Container(
            content=Column(
                controls=[
                    self.user_name,
                    self.title,
                    self.shop,
                    self.myPets,
                    self.out         
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  
            ),
            alignment=alignment.center,  
        )



    
    def verify_pet(self,e):
       
        try:
            pet_df = pd.read_csv(PETS_TABLE_PATH, delimiter=";")
            print("Colunas do CSV:", pet_df.columns)
            if pet_df.loc[pet_df["id_user"] == self.user.id_user].empty:
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
