from flet import *

class Login(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        title_login = Text("Insira seu nome de usuário e senha")
        name = TextField(label = "nome de usuário", width = 300)
        password = TextField(label = "senha", width = 300)
        button = ElevatedButton(text="Avançar", on_click = lambda _: self.page.go('/')) 
        
        return Column(
            controls=[
                title_login,
                name,
                password,
                button
            ]
        )