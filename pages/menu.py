from flet import *

class Menu(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.title = Text("Menu Principal")
        self.shop = ElevatedButton(text = 'Loja', on_click = lambda _: self.page.go('/shop'))  
        self.wash = ElevatedButton(text = 'Banho e Tosa', on_click = lambda _: self.page.go('/')) 
        self.medicine = ElevatedButton(text = 'Veterinária') 
        self.out = ElevatedButton(text='Sair', on_click=self.close_app)    

    def close_app(self, e):
        self.page.window.close()

    def build(self):
        
        return Container(
            content=Column(
                controls=[
                    self.title,
                    self.shop,
                    self.wash,
                    self.medicine,
                    self.out
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  
            ),
            alignment=alignment.center,  
        )

    
