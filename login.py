import flet as ft

class Login:
    def __init__(self, page):
        self.page = page

    def build(self):
        title_login = ft.Text("Insira seu nome de usuário e senha")
        name = ft.TextField(label = "nome de usuário", width = 300)
        password = ft.TextField(label = "senha", width = 300)
        button = ft.ElevatedButton(text="Avançar", on_click = lambda _: self.page.go('/')) 
        
        return page.add(title_login, name, password, button)