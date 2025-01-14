import os
from flet import *
from classes.user import User
from configs import *
from utils import save_user_to_session
import pandas as pd
import csv
import warnings
warnings.filterwarnings("ignore")

class Login(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.title = Text("Insira seu nome de usuário e senha")

        #campos de texto
        self.input_name = TextField(label = "nome de usuário", width = 300,on_submit=self.verify_data)
        self.input_password = TextField(label = "senha", width = 300, on_submit=self.verify_data)

        #buttons
        self.login = ElevatedButton(text="Avançar", on_click = self.verify_data) 
        self.back = ElevatedButton(text="Voltar", on_click = lambda _: self.page.go('/')) 
        
    def build(self):
        return Container(
            content = Column(
                controls=[
                    self.title,
                    self.input_name,
                    self.input_password,
                    self.login,
                    self.back
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )


    #Verifica se um par de valores (nome, senha) existe nos dois primeiros campos de um arquivo CSV.
    def verify_data(self, e):
        try:
            users = pd.read_csv(USERS_TABLE_PATH,sep=";")
            user_match = users[(users["name"] == self.input_name.value) & (users["password"] == self.input_password.value)]
            if not user_match.empty:
                user_data = user_match.iloc[0]                
                user = User(user_data["id_user"],
                            user_data["name"],
                            user_data["password"],
                            user_data["email"],
                            user_data["cpf"],
                            user_data["address"])
                
                save_user_to_session(self.page,user)

                self.page.go('/menu')

            return False  # Retorna False se o par (nome, senha) não for encontrado
        except FileNotFoundError:
            print(f"Erro: Arquivo '{os.path.basename(USERS_TABLE_PATH)}' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False


