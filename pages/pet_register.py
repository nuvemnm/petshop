import os
import shutil
from flet import *
from database.animal_database import AnimalDatabase
from src.user import User
from src.animals import Animal
import pandas as pd
from elements import *
from configs import PETS_TABLE_PATH
from session_manager import load_user_from_session


class PetRegister(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.element = Elements()

        # Título e elementos gráficos
        self.title = self.element.create_title("Cadastre seu bichinho")

        self.padding = Container(height=40)

        # Campos do formulário
        self.specie_input = Dropdown(
            label="Espécie do Animal",
            width=300,
            options=[
                dropdown.Option("Cachorro"),
                dropdown.Option("Gato"),
                dropdown.Option("Peixe"),
            ],
        )
        self.name_input = TextField(label="Nome", width=300)
        self.sex_input = Dropdown(
            label="Sexo",
            width=300,
            options=[
                dropdown.Option("Fêmea"),
                dropdown.Option("Macho"),
            ],
        )
        self.castrated_input = Dropdown(
            label="Castrado",
            width=300,
            options=[
                dropdown.Option("Sim"),
                dropdown.Option("Não"),
            ],
        )
        self.race_input = TextField(label="Raça", width=300)
        self.age_input = TextField(label="Idade", width=300)
        self.weight_input = TextField(label="Peso(kg)", width=300)

        # Botões
        self.upload_button = ElevatedButton(
            "Escolher Foto",
            icon=Icons.UPLOAD_FILE,
            on_click=lambda _: self.pick_files_dialog.pick_files(allow_multiple=False),
            width=300, height=50, style=ButtonStyle(shape=RoundedRectangleBorder(radius=10))
        )
        self.register = self.element.create_button("Finalizar Cadastro", self.verify_data)
        self.back = self.element.create_button("Voltar", lambda _: self.page.go('/home'))


        self.user = load_user_from_session(self.page)
        self.animal_database = AnimalDatabase()

        # Variáveis relacionadas com upload de arquivo
        self.pick_files_dialog = FilePicker(on_result=self.pick_files_result)
        self.selected_file_path = None  # Caminho do arquivo selecionado
        self.has_uploaded_file = False
        page.overlay.append(self.pick_files_dialog)



    def pick_files_result(self, e: FilePickerResultEvent):
        if e.files:
            self.selected_file_path = e.files[0].path  # Caminho do arquivo selecionado
            self.has_uploaded_file = True
            print(f"Arquivo selecionado: {self.selected_file_path}")
        else:
            self.has_uploaded_file = False
            self.selected_file_path = None

    def build(self):
        return Container(
            content=Column(
                controls=[
                    self.title,
                    self.padding,
                    self.specie_input,
                    self.name_input,
                    self.sex_input,
                    self.castrated_input,
                    self.race_input,
                    self.age_input,
                    self.weight_input,
                    self.padding,
                    self.upload_button,
                    self.register,
                    self.back,
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
            alignment=alignment.center,
        )

    def notify_user(self, message):
        dlg = AlertDialog(
            title=Text("Não foi possível cadastrar o animal"),
            content=Text(message),
        )
        self.page.open(dlg)

    def verify_data(self, e):
        try:
            next_id = int(self.animal_database.get_current_id()) + 1

            # Verifica se upload do arquivo já foi realizado
            if not self.has_uploaded_file:
                self.notify_user("O upload de imagem do pet é OBRIGATÓRIO")
                return False
            
            # Código abaixo só roda se o upload de imagem tiver sido realizado
            dest_folder = os.path.join("images", "pets")
            os.makedirs(dest_folder, exist_ok=True)
            if self.selected_file_path:
                file_name = os.path.basename(self.selected_file_path)

            # Define o nome do arquivo e move para a pasta de destino
            dest_path = os.path.join(dest_folder, file_name)

            shutil.copy(self.selected_file_path, dest_path)

            # Criação do objeto Animal com validações via getters e setters
            pet = Animal(next_id, 
            self.user.id_user, 
            self.specie_input.value, 
            self.name_input.value, 
            self.sex_input.value, 
            self.castrated_input.value == "Sim", 
            self.race_input.value, 
            self.age_input.value, 
            self.weight_input.value, 
            dest_path)
     
            if self.animal_database.insert_data(pet):
                self.page.go('/pets')

        except ValueError as ve:
            self.notify_user(str(ve))