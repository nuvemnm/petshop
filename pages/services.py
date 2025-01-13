from flet import *
from classes.animal import Animal
from pets import collect_animals

class Services(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        # Configurações da página
        
        page.padding = 20

        # Botões de ação
        self.wash = ElevatedButton(
            text="Banho e Tosa",
            on_click=lambda _: print("Banho e Tosa clicado!"),
        )
        self.vet = ElevatedButton(
            text="Veterinária?",
            on_click=lambda _: print("Veterinária clicado!"),
        )

        # Imagem do cachorro
        self.dog_image = Image(
            src="https://via.placeholder.com/300",  # Substitua pela URL ou caminho da imagem desejada
            width=300,
            height=200,
            fit="cover",
        )

        # Nome e descrição
        self.name = Text("Tobias", size=25, weight="bold", color="black")
        description = Text(
            "Raça: Golden Retriever\n"
            "Peso: 15Kg\n"
            "Sexo: Macho",
            size=15,
            color="black",
        )

    

    def build(self):

        return container = Container(
                    width=350,
                    padding=10,
                    bgcolor="#f0f0f0",
                    border_radius=10,
                    content=Column(
                        controls=[
                            self.dog_image,
                            self.name,
                            description,
                            Row(
                                controls=[
                                    self.wash,
                                    self.vet,
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                spacing=10,
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                )

