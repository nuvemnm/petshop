from flet import *

class Banho(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.title = Text("Banho e Tosa")
         
        self.payment = ElevatedButton(text = 'Finalizar Pagamento', on_click = lambda _: self.page.go('/pets')) 
        self.back = ElevatedButton(text = 'Voltar', on_click = lambda _: self.page.go('/pets')) 
    
    def build(self):
        
        return Container(
            content=Column(
                controls=[
                    self.title,
                    self.payment,
                    self.back
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )

    
