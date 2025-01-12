from flet import *

class Menu(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.title = Text("Menu Principal")
        self.shop = ElevatedButton(text = 'Loja', on_click = lambda _: self.page.go('/'))  
        self.wash = ElevatedButton(text = 'Banho e Tosa', on_click = lambda _: self.page.go('/')) 
        self.medicine = ElevatedButton(text = 'Veterinária') 
    
    def build(self):
        
        return Container(
            content=Column(
                controls=[
                    self.title,
                    self.shop,
                    self.wash,
                    self.medicine
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )

    
