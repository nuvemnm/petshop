class Animal:
    def __init__(self, id_pet=None, id_user=None, specie=None, name=None, sex=None, castrated=None, race=None, age=None, weight=None, image=None):
        self.id_pet = id_pet
        self.id_user = id_user
        self.specie = specie
        self.name = name
        self.sex = sex
        self.castrated = castrated
        self.race = race
        self.age = age
        self.weight = weight
        self.image = image

    # Getter e Setter para 'id_pet'
    @property
    def id_pet(self):
        return self._id_pet

    @id_pet.setter
    def id_pet(self, value: str):
        self._id_pet = value

    # Getter e Setter para 'id_user'
    @property
    def id_user(self):
        return self._id_user

    @id_user.setter
    def id_user(self, value: str):
        self._id_user = value

    # Getter e Setter para 'specie'
    @property
    def specie(self):
        return self._specie

    @specie.setter
    def specie(self, value: str):
        if not value:
            raise ValueError("A espécie é obrigatória.")
        self._specie = value

    # Getter e Setter para 'name'
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("O nome do animal é obrigatório.")
        if len(str(value)) < 2:
            raise ValueError("O nome deve ter pelo menos 2 caracteres.")
        self._name = value

    # Getter e Setter para 'sex'
    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, value: str):
        if value not in ["Macho", "Fêmea"]:
            raise ValueError("O sexo deve ser 'Macho' ou 'Fêmea'.")
        self._sex = value

    # Getter e Setter para 'castrated'
    @property
    def castrated(self):
        return self._castrated

    @castrated.setter
    def castrated(self, value: str):
        if not value:
            raise ValueError("O status de castração deve ser preenchido.")
        self._castrated = value

    # Getter e Setter para 'race'
    @property
    def race(self):
        return self._race

    @race.setter
    def race(self, value: str):
        if not value:
            raise ValueError("A raça é obrigatória.")
        self._race = value

    # Getter e Setter para 'age'
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value : str):
        if not str(value).strip():
            raise ValueError("A idade não pode ser vazia.")
        try:
            value = int(value)
        except ValueError:
            raise ValueError("A idade deve ser um número inteiro válido.")
        if value < 0:
            raise ValueError("A idade deve ser um número inteiro maior ou igual a 0.")
        self._age = value


    # Getter e Setter para 'weight'
    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value : str):
        if not str(value).strip():
            raise ValueError("O peso não pode ser vazio.")
        try:
            value = float(value)
        except ValueError:
            raise ValueError("O peso deve ser um número válido.")
        if value <= 0:
            raise ValueError("O peso deve ser maior que 0.")
        self._weight = value

    # Getter e Setter para 'image'
    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value: str):
        self._image = value
