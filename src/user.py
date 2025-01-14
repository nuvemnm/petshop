import re


class User:
    def __init__(self, id_user = None, name=None, password=None, email=None, cpf=None, address=None):
        self.id_user = id_user
        self.name = name
        self.password = password
        self.email = email
        self.cpf = cpf
        self.address = address

    # Getter e Setter para 'id_user'
    @property
    def id_user(self):
        return self._id_user

    @id_user.setter
    def id_user(self, value: str):
        self._id_user = value


    # Getter e Setter para 'name'
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("O nome é obrigatório")
        if len(str(value)) < 5:
            raise ValueError("O nome deve ter pelo menos 5 caracteres.")
        self._name = value

    # Getter e Setter para 'password'
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        if not password:
            raise ValueError("A senha é obrigatória.")
        # Verifica se a senha tem pelo menos 8 caracteres
        if len(str(password)) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")

        # Verifica se a senha contém pelo menos um símbolo
        if not re.search(r'[^\w\s]', password):  # Regex
            raise ValueError("A senha deve conter pelo menos um símbolo.")

        self._password = password


    # Getter e Setter para 'email'
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if not email:
            raise ValueError("O email é obrigatório.")
        allowed_domains = ["@gmail.com", "@hotmail.com", "@outlook.com", "@yahoo.com", "@ufmg.br"]
        if not any(email.endswith(domain) for domain in allowed_domains):
            raise ValueError(f"O email deve ser de um dos seguintes domínios: {', '.join(allowed_domains)}.")
        self._email = email

    # Getter e Setter para 'cpf'
    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, cpf : str):
        if not cpf:
            raise ValueError("O CPF é obrigatório.")
        
        # Verifica se o CPF tem exatamente 11 caracteres numéricos
        if len(str(cpf)) != 11 or not str(cpf).isdigit():
            raise ValueError("O CPF deve conter 11 dígitos.")
        self._cpf = cpf

    # Getter e Setter para 'address'
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if not address:
            raise ValueError("O endereço é obrigatório.")
        self._address = address
