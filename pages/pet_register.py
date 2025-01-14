import os
import shutil
from flet import *
from classes.user import User
from classes.animals import Animal
import pandas as pd
from elements import *
from configs import PETS_TABLE_PATH
from utils import load_user_from_session,save_user_pets_to_session


class PetRegister(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.element = Elements()

        self.padding = Container(height=40)
        
        self.user = load_user_from_session(self.page)
        
        # Título
        self.title = self.element.create_title("Cadastre seu bichinho")
        
        # FilePicker para seleção de imagem
        self.pick_files_dialog = FilePicker(on_result=self.pick_files_result)
        self.selected_file_path = None  # Caminho do arquivo selecionado
        page.overlay.append(self.pick_files_dialog)

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
            width = 300, height = 50, style=ButtonStyle(shape=RoundedRectangleBorder(radius=10))
        )
        self.register = self.element.create_button("Finalizar Cadastro", self.verify_data)
        self.back = self.element.create_button("Voltar", lambda _: self.page.go('/pets'))

    def get_current_id(self):
        try:
            data = pd.read_csv(PETS_TABLE_PATH, sep=";")
            max_id = max(pd.read_csv(PETS_TABLE_PATH,sep=";")["id_pet"].values)
            return max_id or 0
        except Exception as e:
            print(f"Erro ao obter ID atual: {e}")
            return 0

    def pick_files_result(self, e: FilePickerResultEvent):
        if e.files:
            self.selected_file_path = e.files[0].path  # Caminho do arquivo selecionado
            print(f"Arquivo selecionado: {self.selected_file_path}")
        else:
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
    
    def notify_user(self,message):
        dlg = AlertDialog(
            title=Text("Não foi possível cadastras o animal"),
            content=Text(message),
        )
        self.page.open(dlg)

    def verify_data(self, e):
        try:
            next_id = self.get_current_id() + 1

            dest_folder = os.path.join("images", "pets")
            os.makedirs(dest_folder, exist_ok=True)

            # Define o nome do arquivo e move para a pasta de destino
            file_name = os.path.basename(self.selected_file_path)
            dest_path = os.path.join(dest_folder, file_name)
            
            shutil.copy(self.selected_file_path, dest_path)

            pet = Animal(next_id, self.user.id_user, self.specie_input.value, self.name_input.value, self.sex_input.value, self.castrated_input.value, self.race_input.value, self.age_input.value, self.weight_input.value, dest_path)
            self.insert_data(pet)

        except ValueError as ve:
            self.notify_user(ve)


    def insert_data(self, animal):
        print(animal.age)
        line = f"{animal.id_pet};{animal.id_user};{animal.specie};{animal.name};{animal.sex};{animal.castrated};{animal.race};{animal.age};{animal.weight};{animal.image}"
        
        try:

            # Insere a linha no CSV
            with open(PETS_TABLE_PATH, 'a', encoding='utf-8') as f:
                f.write(line + '\n')

                print(f"Cadastro realizado com sucesso: {line}")
                save_user_pets_to_session(self.page, self.user.id_user)

                self.page.go('/menu')

        except Exception as ex:
            print(f"Erro ao inserir os dados: {ex}")
