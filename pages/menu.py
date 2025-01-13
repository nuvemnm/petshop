from flet import *
import csv
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

    
    def verify_pet(self, e):
       
        try:
            with open("csv\\animals.csv", mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                # Itera sobre cada linha do arquivo CSV
                #next(reader)
                for linha in reader:
                    # Garante que a linha tem pelo menos dois campos
                    if linha[0] == self.user.id_user:
                        print(self.user.id_user)
                        self.page.go('/pets')
                    else:
                        self.page.go('/pet_register')

            return False  
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo}' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False
