from flet import *
from pages.home import Home
from pages.login import Login
from pages.register import Register
from pages.menu import Menu
from pages.shop import Shop

def views_handler(page):
    return {
        '/': View(route  = '/', controls = [Home(page)]),
        '/login': View(route = '/login', controls = [Login(page)]),
        '/register' : View(route = '/register', controls = [Register(page)]),
        '/menu' : View(route = '/menu', controls = [Menu(page)]),
        '/shop' : View(route = '/shop', controls = [Shop(page)])
    }