class ConnectionError(Exception):
    def __str__(self):
        return "Could not connect to server: Invalid host or port"

class InvalidCredentialsError(Exception):
    def __str__(self):
        return "Could not connect due invalid credentials (username or password)"

class RouteNotFoundError(Exception):
    def __str__(self):
        return "The received route does not exist"
