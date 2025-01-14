from flet import *
from database.product_database import ProductDatabase
from database.purchases_database import PurchasesDatabase
from session_manager import *
from pages.cart import *
from elements import *
from configs import *
from shopping_cart import Shopping_Cart

class Payment(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.element = Elements()

        self.back = self.element.create_button("Voltar", lambda _: self.page.go('/menu'))

        self.user = load_user_from_session(self.page)

        self.payment_info = self.page.session.get("payment_info")

        self.product_database = ProductDatabase()
        self.purchases_database = PurchasesDatabase()

        self.price = self.element.create_title(f"Subtotal: R$ 0")

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
        if not self.payment_info:
            return
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



        if self.payment_info["origin_page"] == "cart":
            for _, product in self.payment_info["products"].iterrows():
                # Itera pela quantidade do produto
                for _ in range(int(product["quantity"])):  # A quantidade determina o número de repetições
                    # Passa cada produto para o método de inserção de compra
                    self.purchases_database.insert_purchase(self.user, "cart", product)
                    
                    # Decrementa a quantidade do produto no banco de dados de produtos
                    self.product_database.decrease_item(product)
                
            # Limpa o carrinho
            self.page.session.set("cart", Shopping_Cart())

        elif self.payment_info["origin_page"] == "wash":
            # Passa cada produto para o método de inserção de compra
            self.purchases_database.insert_purchase(self.user, "wash", self.payment_info["products"])
            


        self.page.go('/menu')
        return True  # Retorna True para indicar que a validação foi bem-sucedida



    def build(self):
        self.payment_info = self.page.session.get("payment_info")
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
