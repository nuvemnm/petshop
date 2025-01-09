import flet as ft

pages = None

def initPage(page: ft.Page):

   

    title = ft.Text("Página Inicial")
    login = ft.ElevatedButton(text = 'Login', on_click = switch) 
    register = ft.ElevatedButton(text = 'Cadastrar') 
    out = ft.ElevatedButton(text = 'Sair') 

    page.add(title, login, register, out)

    pass

def loginPage(page: ft.Page):
    name = ft.TextField(label = "nome de usuário", width = 300)
    title = ft.Text("Insira seu nome de usuário e senha")
    password = ft.TextField(label = "senha", width = 300)
    
    def verify(e):
        if not name.value or not name.value.strip():
            # Mensagem de erro
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Erro: O campo 'Nome de usuário' está vazio.", color="white"),
                bgcolor="red",
            )
        else:
            # Mensagem de sucesso
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Bem-vindo, {name.value}!", color="white"),
                bgcolor="green",
            )
        page.snack_bar.open = True  # Exibe o SnackBar
        page.update()

    button = ft.ElevatedButton(text="Avançar", on_click = verify)
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    page.add(title, name, password, button)

    
ft.app(target = loginPage)