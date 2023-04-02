from lib.client_server import Server
from lib.parsers import ServerParser as Parser

# Create a parser for the command line arguments from the ServerParser class
cmd_parser = Parser()
args = cmd_parser.parse()

# Create a server object and start it using the command line arguments
server = Server(args.server, args.port)
server.start()
