from flet import *

class Home(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        title = Text("Página Inicial")
        login = ElevatedButton(text = 'Login', on_click = lambda _: self.page.go('/login'))  
        register = ElevatedButton(text = 'Cadastrar') 
        out = ElevatedButton(text = 'Sair') 
        
        return Column(
            controls=[
                title,
                login,
                register,
                out
            ]
        )

    
