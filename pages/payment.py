from flet import *
from session_manager import *
from pages.cart import *
from elements import *
from configs import *

class Payment(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.element = Elements()

        self.back = self.element.create_button("Voltar", lambda _: self.page.go('/menu'))

        self.user = load_user_from_session(self.page)

        self.payment_info = self.page.session.get("payment_info")
        if self.payment_info:
            self.price = self.element.create_title(f"Subtotal: R$ {self.payment_info['price']}")

            self.back = self.element.create_button("Voltar", lambda _: self.page.go(f'/{self.payment_info["origin_page"]}'))
            
        self.image_path = "images/especial/Untitled.png" 
        self.title = self.element.create_title("Pagamento")
        self.input_name = TextField(label="Nome de usuário", width=300)
        self.input_address = TextField(label="Endereço", width=300)
        
        if self.user:
            self.input_name = TextField(label="Nome de usuário", width=300, value=self.user.name,read_only=True,text_style=TextStyle(color=colors.GREY))
            self.input_address = TextField(label="Endereço", width=300,value=self.user.address,read_only=True,text_style=TextStyle(color=colors.GREY))

        self.number_card = TextField(label="Número do Cartão", width=300)
        self.cvv = TextField(label="CVV", width=140)
        self.validade = TextField(label="Validade", width=140)

        # RadioGroup com opções
        # RadioGroup com opções
        self.radio_input = RadioGroup(
                content=Column(
                    [
                        Radio(value="debito", label="Cartão de Débito"),
                        Radio(value="credito", label="Cartão de Crédito"),
                        Radio(value="pix", label="Pix"),
                    ],
                ),
                on_change=self.radiogroup_changed,
            )
    


        # Um contêiner dinâmico que será atualizado conforme a seleção
        self.dynamic_container = Container()

        # Botão de voltar
        self.pay = self.element.create_button("Finalizar Pagamento", self.verify_data)

    def radiogroup_changed(self, e):
        # Limpa os controles existentes do contêiner dinâmico
        self.dynamic_container.content = None

        # Atualiza o conteúdo do contêiner dinamicamente com base na seleção
        if e.control.value == "debito" or e.control.value == "credito":
            self.dynamic_container.content = Container(
                content=Column(
                    controls=[
                        self.number_card,
                        Row(
                            controls=[
                                self.cvv,
                                self.validade,
                            ],
                            alignment=MainAxisAlignment.CENTER,  # Centraliza a Row horizontalmente
                        ),
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza horizontalmente os elementos da Column
                ),
                alignment=alignment.center,  # Centraliza o Container na tela
                padding=20,
            )
        elif e.control.value == "pix":
            self.dynamic_container.content = Container(
                content=Column(
                    controls=[
                        Text("Escaneie o QRCode", size=24, text_align="center"),
                        Image(src=self.image_path, width=300, height=300, fit="contain"),
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza horizontalmente os elementos da Column
                ),
                alignment=alignment.center,  # Centraliza o Container na tela
                padding=20,
            )



        # Atualiza a página para refletir as alterações
        self.dynamic_container.update()
 
    def verify_data(self, e):
        # Lista para armazenar mensagens de erro
        errors = []

        # Verifica se os campos obrigatórios estão preenchidos
        if not self.input_name.value.strip():
            errors.append("O campo 'Nome de usuário' deve ser preenchido.")
        if not self.input_address.value.strip():
            errors.append("O campo 'Endereço' deve ser preenchido.")

        # Valida os campos de cartão de crédito/débito se a opção correspondente for selecionada
        if self.radio_input.value in ["debito", "credito"]:
            if not self.number_card.value.strip() or not self.number_card.value.isdigit():
                errors.append("O campo 'Número do Cartão' deve conter apenas números.")
            if not self.cvv.value.strip() or not self.cvv.value.isdigit():
                errors.append("O campo 'CVV' deve conter apenas números.")
            if not self.validade.value.strip() or not self.validade.value.replace("/", "").isdigit():
                errors.append("O campo 'Validade' deve conter apenas números e o formato MM/AA.")

        # Se houver erros, exibe-os no console
        if errors:
            for error in errors:
                dlg = AlertDialog(
                    title=Text("Não foi possível finalizar o pagamento"),
                    content=Text(error),
                )
                self.page.open(dlg)
            return False  # Retorna False para indicar que a validação falhou

        # Todos os campos foram validados com sucesso
        print("Todos os campos foram preenchidos corretamente!")
        self.insert_purchase()
        if self.payment_info["origin_page"] == "cart":
            self.decrease_item()

        self.page.go('/menu')
        return True  # Retorna True para indicar que a validação foi bem-sucedida
        
    def get_current_id(self):
        df = pd.read_csv(PURCHASES_TABLE_PATH, sep=";")
        
        if df.empty:
            return 0
        
        max_id = df["id_purchase"].max() 
        return int(max_id) if pd.notna(max_id) else 0


    def insert_purchase(self):
        if self.payment_info["origin_page"] == "cart":
            purchases_df = pd.read_csv(PURCHASES_TABLE_PATH, sep=";")

            new_rows = []
            for item in self.payment_info["products"].itertuples(index=False):
                # Repetir o item com base na quantidade
                for _ in range(int(item.quantity)):  # A quantidade é usada para determinar a repetição
                    new_rows.append({
                        "id_purchase":self.get_current_id()+1,
                        "id_product": item.id_product,
                        "id_user":self.user.id_user,
                        "name": item.name,
                        "price": item.price,
                        "date": pd.to_datetime("today").strftime("%Y-%m-%d"),  # Data de compra
                        "description": item.description,
                        "image": item.image,
                        "status": "Preparando pedido"
                    })
            # Criar um DataFrame para as novas linhas
            new_df = pd.DataFrame(new_rows)

            # Adicionar as novas linhas ao DataFrame existente
            purchases_df = pd.concat([purchases_df, new_df], ignore_index=True)

            # Salvar o DataFrame atualizado no CSV, preservando as informações existentes
            purchases_df.to_csv(PURCHASES_TABLE_PATH, sep=";", index=False)
        
        elif self.payment_info["origin_page"] == "wash":
            print("INSERINDO WASH")
            item = self.payment_info["products"]
            purchases_df = pd.read_csv(PURCHASES_TABLE_PATH, sep=";")
            new_rows = []
            new_rows.append({
                "id_purchase":self.get_current_id()+1,
                "id_service": item["id_service"],
                "id_user":self.user.id_user,
                "name": item["name"],
                "price": item["price"],
                "date": pd.to_datetime("today").strftime("%Y-%m-%d"),  # Data de compra
                "status": "Aguardando data"
            })
            # Criar um DataFrame para as novas linhas
            new_df = pd.DataFrame(new_rows)

            # Adicionar as novas linhas ao DataFrame existente
            purchases_df = pd.concat([purchases_df, new_df], ignore_index=True)

            # Salvar o DataFrame atualizado no CSV, preservando as informações existentes
            purchases_df.to_csv(PURCHASES_TABLE_PATH, sep=";", index=False)


    def decrease_item(self):
        products_df = pd.read_csv(PRODUCTS_TABLE_PATH, sep=";")
        
        if not products_df.empty:
            for item in self.payment_info["products"].itertuples(index=False):
                product_index = products_df[products_df["id_product"] == item.id_product].index
                
                if len(product_index) > 0:
                    # Reduzir a quantidade do produto encontrado
                    products_df.at[product_index[0], "quantity"] -= 1
                    
            # Salvar as alterações de volta no arquivo CSV
            products_df.to_csv(PRODUCTS_TABLE_PATH, sep=";", index=False)
        else:
            print("Não há produtos no inventário.")


    def build(self):
        print(self.payment_info)
        return Container(
            content=Column(
                controls=[
                    self.title,
                    self.price,
                    self.input_name,
                    self.input_address,
                    self.radio_input,  # RadioGroup centralizado
                    self.dynamic_container,  # Contêiner dinâmico
                    self.pay,
                    self.back,
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente
            ),
            alignment=alignment.center,  # Centraliza todo o container na página
        )
