class Error(Exception):
    pass


class Unauthorized(Exception):
    pass


class NotFound(Exception):
    pass


class TooManyRequests(Exception):
    pass


class UserNotFound(Exception):
    pass


def handle(response):
    if response['error'] == 'Unauthorized':
        raise Unauthorized(response['message'])
    elif response['error'] == 'Not Found':
        raise NotFound(response['message'])
    elif response['error'] == 'Too Many Requests':
        raise TooManyRequests(response['message'])
    else:
        raise Exception(response)
