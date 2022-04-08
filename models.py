from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id: int, email: str, password: str):
        self.id = user_id
        self.email = email
        self.password = password
        self.authenticated = False

    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def get_id(self):
        return self.id
