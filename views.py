from flet import *
from pages.home import Home
from pages.login import Login
from pages.register import Register
from pages.menu import Menu
from pages.shop import Shop
from pages.cart import Cart
from pages.banho import Banho
from pages.pets import Pets
from pages.pet_register import PetRegister
from pages.banho import Banho
## from pages.services import Services

def views_handler(page):
    return {
        '/': View(route  = '/', controls = [Home(page)]),
        '/login': View(route = '/login', controls = [Login(page)]),
        '/register' : View(route = '/register', controls = [Register(page)]),
        '/menu' : View(route = '/menu', controls = [Menu(page)]),
        '/shop' : View(route = '/shop', controls = [Shop(page)]),
        '/cart' : View(route = '/cart', controls = [Cart(page)]),
        '/pets' : View(route = '/pets', controls = [Pets(page)]),
        '/pet_register' : View(route = '/pet_register', controls = [PetRegister(page)]),
        '/wash' : View(route = '/wash', controls = [Banho(page)]),
        #'/veterinia' : View(route = '/veterinaria', controls = [Services(page)])
    }