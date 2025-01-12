from flet import *

class Register(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        
        self.title = Text("Cadastro")

        #campos de texto
        self.name = TextField(label = "nome de usuário", width = 300)
        self.email = TextField(label = "Email", width = 300)
        self.cpf = TextField(label = "CPF", width = 300)
        self.address = TextField(label = "Endereço", width = 300)
        self.password = TextField(label = "Senha", width = 300)
        
        #buttons
        self.register = ElevatedButton(text = 'Finalizar Cadastro', on_click = self.insert_data) 
        self.back = ElevatedButton(text = 'Voltar', on_click = lambda _: self.page.go('/'))

    def build(self):
        
        return Container(
            content = Column(
                controls=[
                    self.title,
                    self.name,
                    self.email,
                    self.cpf,
                    self.address,
                    self.password,
                    self.register,
                    self.back
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )
    
    #Insere uma linha de dados em um arquivo CSV no formato de string.
    def insert_data(self, e):
        
        line = f"{self.name.value},{self.password.value},{self.email.value},{self.cpf.value},{self.address.value}"   
        
        try:
            # Abre o arquivo em modo de anexar
            with open("csv\\users.csv", 'a', encoding='utf-8') as f:
                # Adiciona a linha no arquivo e pula para a próxima linha
                f.write(line + '\n')
                self.page.go('/')

            print(f"Linha inserida com sucesso no arquivo '{arquivo}': {linha}")
        except Exception as e:
            print(f"Erro ao inserir a linha no CSV: {e}")
