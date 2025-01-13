from flet import *

class Cart(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.title = Text("Carrinho",size=32)
        self.back = ElevatedButton(text = 'Voltar', on_click = lambda _: self.page.go('/shop')) 
    
    def build(self):
        
        return Container(
            content=Column(
                controls=[
                    self.title,
                    self.back
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )

    