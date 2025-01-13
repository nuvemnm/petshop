import os
from flet import *
from classes.user import User
from configs import USERS_TABLE_PATH
import csv

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
                    self.user.name,
                    self.user.password,
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
            with open(USERS_TABLE_PATH, mode='r', encoding='utf-8') as f:
                leitor = csv.reader(f)
                
                # Itera sobre cada linha do arquivo CSV
                for linha in leitor:
                    # Garante que a linha tem pelo menos dois campos
                    if len(linha) >= 2 and linha[0] == self.user.name.value and linha[1] == self.user.password.value:
                        self.page.go('/menu')

            return False  # Retorna False se o par (nome, senha) não for encontrado
        except FileNotFoundError:
            print(f"Erro: Arquivo '{os.path.basename(USERS_TABLE_PATH)}' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False
