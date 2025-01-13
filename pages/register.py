from flet import *
from classes.user import User
from configs import USERS_TABLE_PATH
import os

class Register(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.user = User()
        
        #titulo
        self.title = Text("Cadastro")

        #campos de texto
        self.user.name = TextField(label = "nome de usuário", width = 300)
        self.user.email = TextField(label = "Email", width = 300)
        self.user.cpf = TextField(label = "CPF", width = 300)
        self.user.address = TextField(label = "Endereço", width = 300)
        self.user.password = TextField(label = "Senha", width = 300)
        
        #buttons
        self.register = ElevatedButton(text = 'Finalizar Cadastro', on_click = self.insert_data) 
        self.back = ElevatedButton(text = 'Voltar', on_click = lambda _: self.page.go('/'))

    def build(self):
        
        return Container(
            content = Column(
                controls=[
                    self.title,
                    self.user.name,
                    self.user.email,
                    self.user.cpf,
                    self.user.address,
                    self.user.password,
                    self.register,
                    self.back
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )
    
    #Insere uma linha de dados em um arquivo CSV no formato de string.
    def insert_data(self, e):
        
        line = f"{self.user.name.value},{self.user.password.value},{self.user.email.value},{self.user.cpf.value},{self.user.address.value}"   
        try:
            # Abre o arquivo em modo de anexar
            with open(USERS_TABLE_PATH, 'a', encoding='utf-8') as f:
                # Adiciona a linha no arquivo e pula para a próxima linha
                f.write(line + '\n')
                self.page.go('/')

            print(f"Linha inserida com sucesso no arquivo '{os.path.basename(USERS_TABLE_PATH)}': {line}")
        except Exception as e:
            print(f"Erro ao inserir a linha no CSV: {e}")
