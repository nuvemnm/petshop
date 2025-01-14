from flet import *
from configs import CHECKMARK_IMG_PATH

class SucessDialog():
    def __init__(self, title, message,page):
        self.page = page
        self.sucess_dialog = AlertDialog(
            title=Text(title),
            content=Row(
                controls=[ 
                    Column(
                        controls=[
                            Image(src=CHECKMARK_IMG_PATH, width=140, height=140, fit="SCALE_DOWN"),  # Imagem menor
                            Text(message, size=20),
                        ],
                        alignment="center",  # Alinhamento centralizado horizontalmente
                        spacing=10
                    )                ],
                alignment="center",  # Definindo o alinhamento corretamente
                spacing=10,
                height=400
            ),
            actions=[
                ElevatedButton(text="OK", on_click=lambda _: self.close())
            ],
        )

    def show(self):
        self.page.open(self.sucess_dialog)

    def close(self):
        self.sucess_dialog.open = False
        self.page.update()