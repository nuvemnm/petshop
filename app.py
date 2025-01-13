from flet import *
from views import views_handler

def main(page: Page):
    # Função chamada quando a rota muda
    def route_change(route):
        print(page.route)
        page.views.clear()
        page.views.append(views_handler(page)[page.route])  # Corrigido "viwes" para "views"
        page.update()

    # Configuração inicial
    page.on_route_change = route_change
    page.go('/')  # Define a página inicial como "/"
    print(page)

app(target=main)
