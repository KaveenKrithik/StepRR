class ArtistNotFoundException(Exception):
    def __init__(self, artist_id: int):
        self.message = f"Artist with id {artist_id} not found"
        self.status_code = 404
        super().__init__(self.message)

class ConcertNotFoundException(Exception):
    def __init__(self, concert_id: int):
        self.message = f"Concert with id {concert_id} not found"
        self.status_code = 404
        super().__init__(self.message)

class RoleNotFoundException(Exception):
    def __init__(self):
        self.message = "Role not found"
        self.status_code = 404
        super().__init__(self.message)

class UserNotFoundException(Exception):
    def __init__(self):
        self.message = "User not found"
        self.status_code = 404
        super().__init__(self.message)

class UserAlreadyExistsException(Exception):
    def __init__(self):
        self.message = "User Already Exists"
        self.status_code = 409
        super().__init__(self.message)
