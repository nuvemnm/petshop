from flet import *

def main(page: Page):
    # Configurações da página
    page.title = "Perfil do Tobias"
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.padding = 20

    # Imagem do cachorro
    dog_image = Image(
        src="https://via.placeholder.com/300",  # Substitua pela URL ou caminho da imagem desejada
        width=300,
        height=200,
        fit="cover",
    )

    # Nome e descrição
    name = Text("Tobias", size=25, weight="bold", color="black")
    description = Text(
        "Raça: Golden Retriever\n"
        "Peso: 15Kg\n"
        "Sexo: Macho",
        size=15,
        color="black",
    )

    # Botões de ação
    banho_tosa_button = ElevatedButton(
        text="Banho e Tosa",
        on_click=lambda _: print("Banho e Tosa clicado!"),
    )
    veterinaria_button = ElevatedButton(
        text="Veterinária?",
        on_click=lambda _: print("Veterinária clicado!"),
    )

    # Estrutura principal
    container = Container(
        width=350,
        padding=10,
        bgcolor="#f0f0f0",
        border_radius=10,
        content=Column(
            controls=[
                dog_image,
                name,
                description,
                Row(
                    controls=[
                        banho_tosa_button,
                        veterinaria_button,
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    spacing=10,
                ),
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )

    page.add(container)


app(target=main)
