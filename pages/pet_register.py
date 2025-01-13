from flet import *
from classes.user import User
from classes.animals import Animal

class PetRegister(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.animal = Animal()

        user_data = page.session.get("user")
        
        #titulo
        self.title = Text("Cadastre seu bichinho")

        #campos de texto
        self.animal.specie = Dropdown(
            label = "Espécie do Animal",
            width=300,
            options=[
                dropdown.Option("Cachorro"),
                dropdown.Option("Gato"),
                dropdown.Option("Peixe"),
            ],
        )
        self.animal.name = TextField(label = "Nome", width = 300)
        self.animal.sex = Dropdown(
            label = "Sexo",
            width=300,
            options=[
                dropdown.Option("Fêmea"),
                dropdown.Option("Macho"),
            ],
        )
        self.animal.castrated = Dropdown(
            label = "Castrado",
            width = 300,
            options = [
                dropdown.Option("Sim"),
                dropdown.Option("Não")
            ],
        )
        self.animal.race = TextField(label = "Raça", width = 300)
        self.animal.age = TextField(label = "Idade", width = 300)
        self.animal.weight = TextField(label = "Peso(kg)", width = 300)
        
        #buttons
        self.register = ElevatedButton(text = 'Finalizar Cadastro', on_click = self.insert_data) 
        self.back = ElevatedButton(text = 'Voltar', on_click = lambda _: self.page.go('/menu'))


    def build(self):
        
        return Container(
            content = Column(
                controls=[
                    self.title,
                    self.animal.specie,
                    self.animal.name,
                    self.animal.sex,
                    self.animal.castrated,
                    self.animal.race,
                    self.animal.age,
                    self.animal.weight,
                    self.register,
                    self.back
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )
    
    #Insere uma linha de dados em um arquivo CSV no formato de string.
    def insert_data(self, e):
        
        line = f"{self.user.id_user},{self.animal.specie.value},{self.animal.name.value},{self.animal.sex.value},{self.animal.castrated.value},{self.animal.race.value},{self.animal.age.value},{self.animal.weight.value}"   
        
        try:
            # Abre o arquivo em modo de anexar
            with open("csv\\animals.csv", 'a', encoding='utf-8') as f:
                # Adiciona a linha no arquivo e pula para a próxima linha
                f.write(line + '\n')
                self.page.go('/menu')

            print(f"Linha inserida com sucesso no arquivo '{arquivo}': {linha}")
        except Exception as e:
            print(f"Erro ao inserir a linha no CSV: {e}")
