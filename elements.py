from flet import *

class Elements:
    def __init__(self, button = None, text = None):
        self.button = button
        self.text = text

    def create_button(self, texto, function):
        return ElevatedButton(text = texto, on_click = function, width = 300, height = 50, style=ButtonStyle(shape=RoundedRectangleBorder(radius=10)))

    def create_title(self, text):
        return Text(text, size = 32, weight = "bold")

    def create_text(self, text):
        return Text(text, size = 20)