class User:
    def __init__(self, author, send):
        self.author = author
        self.send = send

    def change_send(self):
        self.send = not self.send

    def get_send(self):
        return self.send

    def get_author(self):
        return self.author