import os
import shutil
from flet import *
from classes.user import User
from classes.animals import Animal
import pandas as pd
from configs import PETS_TABLE_PATH
from utils import load_user_from_session,save_user_pets_to_session


class PetRegister(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.animal = Animal()
        self.user = load_user_from_session(self.page)
        
        # Título
        self.title = Text("Cadastre seu bichinho")
        
        # FilePicker para seleção de imagem
        self.pick_files_dialog = FilePicker(on_result=self.pick_files_result)
        self.selected_file_path = None  # Caminho do arquivo selecionado
        page.overlay.append(self.pick_files_dialog)

        # Campos do formulário
        self.animal.specie = Dropdown(
            label="Espécie do Animal",
            width=300,
            options=[
                dropdown.Option("Cachorro"),
                dropdown.Option("Gato"),
                dropdown.Option("Peixe"),
            ],
        )
        self.animal.name = TextField(label="Nome", width=300)
        self.animal.sex = Dropdown(
            label="Sexo",
            width=300,
            options=[
                dropdown.Option("Fêmea"),
                dropdown.Option("Macho"),
            ],
        )
        self.animal.castrated = Dropdown(
            label="Castrado",
            width=300,
            options=[
                dropdown.Option("Sim"),
                dropdown.Option("Não"),
            ],
        )
        self.animal.race = TextField(label="Raça", width=300)
        self.animal.age = TextField(label="Idade", width=300)
        self.animal.weight = TextField(label="Peso(kg)", width=300)
        
        # Botões
        self.upload_button = ElevatedButton(
            "Escolher Foto",
            icon=Icons.UPLOAD_FILE,
            on_click=lambda _: self.pick_files_dialog.pick_files(allow_multiple=False),
        )
        self.register = ElevatedButton(text="Finalizar Cadastro", on_click=self.insert_data)
        self.back = ElevatedButton(text="Voltar", on_click=lambda _: self.page.go('/menu'))

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
                    self.animal.specie,
                    self.animal.name,
                    self.animal.sex,
                    self.animal.castrated,
                    self.animal.race,
                    self.animal.age,
                    self.animal.weight,
                    self.upload_button,
                    self.register,
                    self.back,
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
            alignment=alignment.center,
        )
    
    def insert_data(self, e):
        # Verifica se há um arquivo selecionado
        if not self.selected_file_path:
            print("Nenhum arquivo foi selecionado!")
            return
        
        try:
            # Cria o diretório se ele não existir
            dest_folder = os.path.join("images", "pets")
            os.makedirs(dest_folder, exist_ok=True)

            # Define o nome do arquivo e move para a pasta de destino
            file_name = os.path.basename(self.selected_file_path)
            dest_path = os.path.join(dest_folder, file_name)
            print(dest_path)
            shutil.copy(self.selected_file_path, dest_path)
            print("teste 1")
            # Obtem o próximo ID
            next_id = self.get_current_id() + 1
            print("teste 2")
            # Cria a linha de dados
            line = f"{next_id};{self.user.id_user};{self.animal.specie.value};{self.animal.name.value};{self.animal.sex.value};{self.animal.castrated.value};{self.animal.race.value};{self.animal.age.value};{self.animal.weight.value};{dest_path}"
            print(line)
            # Insere a linha no CSV
            with open(PETS_TABLE_PATH, 'a', encoding='utf-8') as f:
                f.write(line + '\n')

            print(f"Cadastro realizado com sucesso: {line}")
            save_user_pets_to_session(self.page, self.user.id_user)

            self.page.go('/menu')

        except Exception as ex:
            print(f"Erro ao inserir os dados: {ex}")
