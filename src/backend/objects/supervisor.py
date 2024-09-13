class Supervisor:
    def __init__(self, name: str, email: str | None = None):
        self.name = name
        self.email = email

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email
