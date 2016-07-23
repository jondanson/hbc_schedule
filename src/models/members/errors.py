
class MemberError(Exception):
    def __init__(self, message):
        self.message = message


class MemberNotExistError(MemberError):
    pass

class InvalidEmailError(MemberError):
    pass




