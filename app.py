from flet import *
from views import views_handler
from configs import *
import warnings
warnings.filterwarnings("ignore")

def main(page: Page):
    page.window.height = APP_HEIGHT
    page.window.width = APP_WIDTH
    page.window.center()

    # Função chamada quando a rota muda
    def route_change(route):
        print(page.route)
        page.views.clear()
        page.views.append(views_handler(page)[page.route])
        page.update()

    # Configuração inicial
    page.on_route_change = route_change
    page.go('/shop') 

app(target=main)
