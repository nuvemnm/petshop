import flet as ft

class Home:
    def __init__(self, page):
        self.page = page

    def build(self):
        title = ft.Text("Página Inicial")
        login = ft.ElevatedButton(text = 'Login', on_click = lambda _: self.page.go('/login'))  
        register = ft.ElevatedButton(text = 'Cadastrar') 
        out = ft.ElevatedButton(text = 'Sair') 
        
        controls = [page.add(title, login, register, out)]
        return controls
