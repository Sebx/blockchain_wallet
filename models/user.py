from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, node_identifier, active=True):
        self.id = id
        self.node_identifier = node_identifier
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        pass