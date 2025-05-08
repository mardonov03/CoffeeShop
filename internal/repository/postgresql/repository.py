from internal.repository.postgresql.user import UserRepository

class UserRepo:
    def __init__(self, conn):
        self.user = UserRepository(conn)