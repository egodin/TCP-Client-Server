import sys

from lib.client_server import Client
from lib.parsers import ClientParser as Parser

# Create a parser for the command line arguments from the ClientParser class
cmd_parser = Parser()
args = cmd_parser.parse()

# Create a client object and connect to the server using the command line arguments
client = Client(args.server, args.port)
client.connect()
client.init()

# main control loop
while True:
    command = input("Enter command: ")
    if not command:
        # Fill command with a default value to avoid sending an empty string, and continue the loop
        command = 0
        continue

    if command == "EXIT":
        # Disconnect from the server and exit the program
        client.disconnect()
        sys.exit(0)

    # Send the command to the server and print the response
    response = client.send_command(command)
    print(response)
    if "DISCONNECTED" in response:
        # Disconnect from the server and exit the program
        client.disconnect()
        sys.exit(0)




