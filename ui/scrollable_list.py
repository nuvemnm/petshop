from flet import *
import pandas as pd

class Scrollable_list:
    def __init__(self, dataframe: pd.DataFrame, title_col_name: str, desc_col_names: dict, on_item_click):
        self.dataframe = dataframe
        self.title_col_name = title_col_name
        self.desc_col_names = desc_col_names
        self.on_item_click = on_item_click

    def build(self):
        cards = []

        for _, item in self.dataframe.iterrows():
            image_url = item.get("image", None)
            
            card_height = 210 if image_url else 150
            
            card = GestureDetector(
                on_tap=lambda e, p=item: self.on_item_click(p),
                content=Card(
                    content=Container(
                        padding=10,
                        content=Row(
                            controls=[
                                Image(
                                    src=image_url,
                                    height=180,
                                    width=180,
                                    fit="FIT_HEIGHT"
                                ) if image_url else Container(),
                                
                                Column(
                                    controls=[
                                        Text(item[self.title_col_name], size=26, weight="bold"),
                                        *[
                                            Text(f"{label}: {item[col]}", size=18)
                                            for col, label in self.desc_col_names.items()
                                        ],
                                    ],
                                    alignment="start",
                                    spacing=5,
                                ),
                            ],
                            alignment="start",
                            spacing=10,
                        ),
                    ),
                    width=240,
                    height=card_height,
                ),
            )
            cards.append(card)

        return ListView(
            controls=cards,
            spacing=10,
            padding=10,
            height=500,
        )
