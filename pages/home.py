from flet import *

class Home(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.title = Text("Página Inicial")
        self.login = ElevatedButton(text = 'Login', on_click = lambda _: self.page.go('/login'))  
        self.register = ElevatedButton(text = 'Cadastrar', on_click = lambda _: self.page.go('/register')) 
        self.out = ElevatedButton(text = 'Sair') 
    
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

    
