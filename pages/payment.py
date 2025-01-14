from flet import *

class Payment(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.title = Text("Pagamento")
         
        self.back = ElevatedButton(text = 'Voltar', on_click = lambda _: self.page.go('/cart')) 
    
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

    
