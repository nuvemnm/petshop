import flet as ft
from views import views_handler

def main(page: ft.Page):

    def route_change(route):
        print(page.route)
        page.views.clear()
        page.viwes.append(
            views_handler(page)[page.route]
        )

        page.on_route_change = route_change
        page.go("/")

    
ft.app(target = main)
            