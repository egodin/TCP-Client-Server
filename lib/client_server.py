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

    def init(self) -> None:
        """
        Receive the welcome package from the server
        :return: None
        """
        # initialize the data_received variable to an empty string
        data_received = ''

        # Keep receiving data until the newline separator is received
        while '\n' not in data_received:
            data_received += self.socket.recv(1024).decode()

        # Split the received data into the server IP and the welcome message based on the newline separator
        server_ip, welcome_message = data_received.split('\n')

        # Print the server IP and the welcome message
        print("Server IP:", server_ip)
        print(welcome_message)

    def send_command(self, command) -> str:
        """
        This method sends a command to the server and returns the received response
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
    """
    Simple server class for a socket-based server
    """

    def __init__(self, server_address, server_port) -> None:
        """
        Initialize the server using provided parameters to feed the methods with the instance socket. Arguments are
        strings provided by the parser
        :param server_address: server IP address
        :param server_port: server port number
        :return: None
        """
        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((server_address, server_port))

    def start(self) -> None:
        """
         Start the server and listen for incoming connections
         :return: None
         """
        # Listen for incoming connections. Parameter is set to 5 to prevent server hangs
        self.socket.listen(5)

        # Print the server IP address and port number on the server side console on launch
        print(f"Server listening on {self.server_address}:{self.server_port}")

        # Accept incoming connections, print the client IP address on server side console
        while True:
            conn, addr = self.socket.accept()
            print(f"Connection from {addr}")

            # call init() method to send welcome message to the client on initial connection
            welcome_string = self.init()
            conn.sendall(welcome_string.encode())

            # main control loop
            while True:
                try:
                    # Set a timeout for receiving data from the client
                    conn.settimeout(20)  # 20 seconds timeout
                    data = conn.recv(1024).decode()

                    # If no data is received, break the loop
                    if not data:
                        break

                    # Process the received data and send response
                    match data:
                        case 'TIME':
                            # Get the current time on server and send it to the client
                            response = time.ctime(time.time()) + "\r\n"
                            conn.send(response.encode())
                        case 'IP':
                            # Get the IP address of the client and send it
                            response = addr[0] + "\r\n"
                            conn.send(response.encode())
                        case 'OS':
                            # Get the OS of the server, send it to the client
                            response = "OS: " + sys.platform + "\r\n"
                            conn.send(response.encode())
                        case 'FICHIER':
                            # Send a file to the client
                            filename = 'file.txt'
                            file = open(filename, 'rb')
                            line = file.read(1024)
                            # Keep sending data to the client until the file is fully sent
                            while line:
                                conn.send(line)
                                line = file.read(1024)
                            file.close()
                        case _:
                            # Invalid command: print allowed commands to the client
                            response = "Invalid command. Valid commands are TIME, IP, OS, FICHIER, EXIT.\r\n"
                            conn.send(response.encode())

                except socket.timeout:
                    # Handle timeout: close the connection and reset for a new incoming connection
                    # DISCONNECTED is expected by the client and will close on the client side as well
                    print("Timeout occurred")
                    conn.send("DISCONNECTED. Closing the connection.".encode())
                    conn.close()
                    break

            # Close the connection
            conn.close()

    def init(self) -> str:
        """
        Prepare a welcome message package for the client
        :return: string containing the server IP and the welcome message
        """
        # get the server IP address
        server_ip = self.server_address
        welcome_message = "Welcome to the ETIENNE.GODIN@CR430 server! Valid commands are TIME, IP, OS, FICHIER, EXIT."

        # Concatenate the server IP and the welcome message, return the result
        welcome_string = server_ip + '\n' + welcome_message
        return welcome_string
