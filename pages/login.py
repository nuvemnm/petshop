import os
from flet import *
from database.user_database import UserDatabase
from src.user import User
from ui.elements import *
from configs import *
from session_manager import save_user_to_session
import pandas as pd
import csv
import warnings
warnings.filterwarnings("ignore")

class Login(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.user_database = UserDatabase()
        self.element = Elements()
        self.title = self.element.create_title("Insira seu nome de usuário e senha")
        self.padding = Container(height=40)
        #campos de texto
        self.input_name = TextField(label = "nome de usuário", width = 300,on_submit=self.verify_data)
        self.input_password = TextField(label = "senha", width = 300, on_submit=self.verify_data)

        #buttons
        self.login = self.element.create_button("Avançar", self.verify_data) 
        self.back = self.element.create_button("Voltar", lambda _: self.page.go('/'))
        
    def build(self):
        return Container(
            content = Column(
                controls=[
                    self.title,
                    self.padding,
                    self.input_name,
                    self.input_password,
                    self.padding,
                    self.login,
                    self.back
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )

    #Verifica se o par usuário e senha inserido existe no BD
    def verify_data(self, e):
        try:
            user_match = self.user_database.get_user_with_username_and_password(self.input_name.value,self.input_password.value)

            if user_match.empty:
                dlg = AlertDialog(
                title=Text("Não foi possível fazer login."),
                content=Text("Usuário ou senha incorretos"),
                )   
                self.page.open(dlg)

            else:
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


