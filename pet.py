import flet as ft

def home_page(page: ft.Page):
    return ft.Column(
        [
            ft.Text("Página Inicial", size=30),
            ft.ElevatedButton("Ir para Página 2", on_click=lambda _: page.go("/page2")),
        ]
    )

def page2(page: ft.Page):
    return ft.Column(
        [
            ft.Text("Página 2", size=30),
            ft.ElevatedButton("Voltar para Página Inicial", on_click=lambda _: page.go("/")),
        ]
    )


def main(page: ft.Page):
    page.title = "Navegação com Flet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Função de roteamento
    def route_change(route):
        if page.route == "/":
            page.views.clear()
            page.views.append(ft.View("/", [home_page(page)]))
        elif page.route == "/page2":
            page.views.clear()
            page.views.append(ft.View("/page2", [page2(page)]))
        page.update()

    # Configurações do aplicativo
    page.on_route_change = route_change
    page.go("/")  # Define a página inicial

ft.app(target=main)
