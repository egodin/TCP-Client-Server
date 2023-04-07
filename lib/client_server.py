import socket
import sys
import time


class Client:
    """
    Simple client class for a socket-based server
    """

    def __init__(self, server_address, server_port) -> None:
        """
        Initialize the client using provided parameters to feed the methods with the instance socket
        and the server address
        :param server_address: standard IP address
        :param server_port: start port number
        :return: None
        """
        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        """
        Connect to the server using the instance socket
        :return: None
        """
        self.socket.connect((self.server_address, self.server_port))

    def init(self):
        data_received = ''
        while '\n' not in data_received:  # Keep receiving until newline separator is received
            data_received += self.socket.recv(1024).decode()

        server_ip, welcome_message = data_received.split('\n')  # Split received data into IP and welcome message
        print("Server IP:", server_ip)
        print(welcome_message)

    def send_command(self, command) -> str:
        """
        This method sends a command to the server and returns the response
        :param command: a string command to send to the server
        :return: the string response from the server
        """
        self.socket.send(command.encode())
        response = self.socket.recv(1024).decode()
        return response

    def disconnect(self) -> None:
        """
        Close the connection to the server
        :return: None
        """
        self.socket.close()


class Server:
    def __init__(self, server_address, server_port) -> None:
        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((server_address, server_port))

    def start(self) -> None:
        self.socket.listen(5)
        print(f"Server listening on {self.server_address}:{self.server_port}")
        while True:
            conn, addr = self.socket.accept()
            print(f"Connection from {addr}")

            server_ip = socket.gethostbyname(socket.gethostname())
            welcome_message = "Welcome to the server! Valid commands are TIME, IP, OS, FICHIER, EXIT."
            welcome_string = server_ip + '\n' + welcome_message
            conn.sendall(welcome_string.encode())

            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                match data:
                    case 'TIME':
                        response = time.ctime(time.time()) + "\r\n"
                        conn.send(response.encode())
                    case 'IP':
                        # Get the IP address of the client
                        response = addr[0] + "\r\n"
                        conn.send(response.encode())
                    case 'OS':
                        # Get the OS of the server
                        response = "OS: " + sys.platform + "\r\n"
                        conn.send(response.encode())
                    case 'FICHIER':
                        # Send a file to the client
                        filename = 'file.txt'
                        file = open(filename, 'rb')
                        line = file.read(1024)
                        # Keep sending data to the client
                        while line:
                            conn.send(line)
                            line = file.read(1024)
                        file.close()
                    case _:
                        # Invalid command: print allowed commands to the client
                        response = "Invalid command. Valid commands are TIME, IP, OS, FICHIER, EXIT.\r\n"
                        conn.send(response.encode())

            conn.close()
