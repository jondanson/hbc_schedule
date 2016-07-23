
class AdminError(Exception):
    def __init__(self, message):
        self.message = message


class AdminNotExistError(AdminError):
    pass


class AdminPasswordNotCorrect(AdminError):
    pass


class AdminAlreadyRegisteredError(AdminError):
    pass


class InvalidEmailError(AdminError):
    pass