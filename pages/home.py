from flet import *
from elements import *

class Home(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.element = Elements()
        self.title = self.element.create_title("Página Inicial")
        self.login = self.element.create_button("Login", lambda _: self.page.go('/login'))
        self.register = self.element.create_button("Cadastrar", lambda _: self.page.go('/register')) 
        self.out = self.element.create_button("Sair", self.close_app)   


    def close_app(self, e):
        self.page.window.close()

    def build(self):
        
        return Container(
            content=Column(
                controls=[
                    self.title,
                    self.login,
                    self.register,
                    self.out
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )

    
