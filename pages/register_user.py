from flet import *
from database.user_database import UserDatabase
from src.user import User
from configs import USERS_TABLE_PATH
from session_manager import save_user_to_session
import pandas as pd

import os

class Register(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        
        #titulo
        self.title = Text("Cadastro")
        self.user_database = UserDatabase()
        #campos de texto
        self.input_name = TextField(label="Nome de usuário", width=300,on_submit=self.verify_data)
        self.input_email = TextField(label="Email", width=300,on_submit=self.verify_data)
        self.input_cpf = TextField(label="CPF", width=300,on_submit=self.verify_data)
        self.input_address = TextField(label="Endereço", width=300,on_submit=self.verify_data)
        self.input_password = TextField(label="Senha", width=300,on_submit=self.verify_data)
        
        #buttons
        self.register = ElevatedButton(text = 'Cadastrar', on_click = self.verify_data) 
        self.back = ElevatedButton(text = 'Voltar', on_click = lambda _: self.page.go('/'))

        self.observations = Text("T͟O͟D͟O͟S͟ os campos são obrigatórios.\n•A senha deve ter no mínimo 8 digitos, e deve ter também um símbolo\n•O CPF deve ter 9 digitos,\n•Domínios de e-mail permitidos: gmail, hotmail, outlook, yahoo, ufmg",
                                 color=colors.GREY)

    def build(self):
        
        return Container(
            content = Column(
                controls=[
                    self.title,
                    self.input_name,
                    self.input_email,
                    self.input_cpf,
                    self.input_address,
                    self.input_password,
                    self.observations,
                    self.register,
                    self.back
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )
    
    
    def verify_data(self, e):
        if self.user_database.is_name_taken(self.input_name.value):
            self.notify_user("O nome de usuário já está em uso.")
            return
        try:
            next_id = self.user_database.get_current_id() + 1
            user = User(next_id,self.input_name.value,self.input_password.value,self.input_email.value,self.input_cpf.value,self.input_address.value)
            self.register_user(user)

        except ValueError as ve:
            self.notify_user(ve)


    
    def notify_user(self,message):
        dlg = AlertDialog(
            title=Text("Não foi possível criar sua conta"),
            content=Text(message),
        )
        self.page.open(dlg)

    # Insere o usuário, salva na sessão e vai pro menu.
    def register_user(self, user):
        self.user_database.insert_data(user)
        save_user_to_session(self.page,user)

        self.page.go('/menu')