from flet import *
import csv
from classes.user import User

class Menu(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.user = User()
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
