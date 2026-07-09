from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome