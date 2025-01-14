from flet import *
import csv
import pandas as pd
from configs import *
from classes.animals import Animal  

class Pets(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.animals = []
        
        self.title = Text("Meus Pets") 
        self.back = ElevatedButton(text='Voltar', on_click=lambda _: self.page.go('/menu'))

    def collect_animals(self):
        try:
            self.animals.clear()  # Limpa a lista antes de recarregar os produtos
            df_pets = pd.read_csv(PETS_TABLE_PATH, delimiter=";")
            with open("csv/animals.csv", mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for line in reader:
                    if len(line) >= 3:
                        id_user, specie, name, sex, castrated, race, age, weight = line
                        self.animals.append(Animal(id_user, specie, name, sex, castrated, race, age, weight))
            return True
        except FileNotFoundError:
            print(f"Erro: Arquivo 'animals.csv' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return False

    def build(self):
        if not self.collect_animals():
            return Text("Erro ao carregar produtos.")

        cards = []
        for animal in self.animals:
            card = Card(
                content=Container(
                    padding=10,
                    content=Column(
                        [
                            Image(src="images/products/biscoito.jpg", height=100, width=100, fit="cover"),
                            Text(animal.name, size=18, weight="bold"),
                            Text(animal.race, size=16),
                            Text(animal.age, size=16),
                        ],
                        alignment="center",
                        spacing=5,
                    ),
                ),
                width=200,
                height=250,
            )
            cards.append(card)

        return Container(
            content=Column(
                controls=[
                    self.title,
                    *cards,  # Adiciona todos os cards
                    self.back,
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )
