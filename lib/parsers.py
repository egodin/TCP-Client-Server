import argparse


class ClientParser:
    """
    Simple class to parse the command line arguments for the client
    """
    def __init__(self) -> None:
        """
        Initialize the parser with the arguments, the server IP and the server port and provide hints
        """
        self.parser = argparse.ArgumentParser(description='Simple client for a socket-based server')
        self.parser.add_argument('-s', '--server', type=str, required=True, help='server address')
        self.parser.add_argument('-p', '--port', type=int, required=True, help='server port')

    def parse(self) -> argparse.Namespace:
        """
        Parse the arguments and return the namespace object to the class that called the method
        :return:
        """
        return self.parser.parse_args()


class ServerParser:
    """
    Simple class to parse the command line arguments for the server
    """
    def __init__(self) -> None:
        """
        Initialize the parser with the arguments, the server IP and the server port and provide hints
        :return: None
        """
        self.parser = argparse.ArgumentParser(description='Simple server for a socket-based server')
        self.parser.add_argument('-s', '--server', type=str, required=True, help='server IP, usually localhost'
                                                                                 'or  0.0.0.0; This needed to be '
                                                                                 'executed as root')
        self.parser.add_argument('-p', '--port', type=int, required=True, help='server port')

    def parse(self) -> argparse.Namespace:
        """
        Parse the arguments and return the namespace object to the class that called the method
        :return: The arguments namespace object
        """
        return self.parser.parse_args()
