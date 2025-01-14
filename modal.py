from flet import *
import pandas as pd


class ItemDetailsModal(UserControl):
    def __init__(self, item: pd.DataFrame, on_close,title_col_name: str, desc: str,buttons_list: list = None):
        super().__init__()
        
        self.item = item
        self.title_col_name = title_col_name

        self.image_url = item.get("image", None) if not item.empty else None

        if self.image_url:
            self.modal_image = Image(width=600, height=400, fit="contain", src=self.image_url)

        self.modal_desc = Text(desc,size=16)

        self.on_close = on_close
        self.buttons_list = buttons_list or []

    def build(self):
        if self.item.empty:
            return AlertDialog(
                modal=True,
                title=Text("Erro", weight="bold"),
                content=Text("Nenhum item foi selecionado."),
                actions=[
                    ElevatedButton(
                        text="Voltar",
                        on_click=lambda _: self.on_close(),
                        expand=True,
                        height=50,
                    )
                ],
            )
        

        content_controls = [
            self.modal_image if self.image_url else Container(), 
            self.modal_desc,
        ]


        return AlertDialog(
            modal=True,
            title=Text(self.item[self.title_col_name], weight="bold"),
            content=Container(
                padding=20,
                content=Column(
                    controls=content_controls,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
            ),
            actions=[
                Row(
                    controls=[
                        *self.buttons_list,
                    ],
                ),
                Container(height=20),  # Remove o espaçamento entre os botões
                Row(
                    controls = [
                        ElevatedButton(
                            text="Voltar",
                            on_click=lambda _: self.on_close(),
                            expand=True,
                            height=50,
                        ),
                    ],
                ),
            ],
        )
