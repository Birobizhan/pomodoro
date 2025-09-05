class UserNotFoundException(Exception):
    detail = "User Not Found"


class UserIncorrectPasswordException(Exception):
    detail = "Incorrect password"


class TokenExpiredException(Exception):
    detail = 'token has expired'


class TokenINCorrectException(Exception):
    detail = "Token is not correct"


class TaskNotFound(Exception):
    detail = 'task not found'
