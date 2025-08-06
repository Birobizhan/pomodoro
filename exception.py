class UserNotFoundException(Exception):
    detail = "User Not Found"


class UserIncorrectPasswordException(Exception):
    detail = "Incorrect password"
