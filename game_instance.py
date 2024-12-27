"""
Metagames Project License

Copyright (c) 2024 Rishat Maksudov

Permission is granted to use, modify, and distribute this software for any purpose, with proper credit to the original author.

This software is provided "as is," without any warranty of any kind. The author is not responsible for any damages arising from its use.

"""


from argparse import ArgumentParser
from metagame_client import start_metagame_client
from metagame_server import start_metagame_server

SERVER_DEFAULT_HOST = '127.0.0.1'
SERVER_DEFAULT_PORT = 8808

def run_server(ip, port):
    """
    Starts the Metagame server on the specified IP and port.

    Args:
        ip (str): IP address for the server to bind to.
        port (int): Port for the server to listen on.
    """
    start_metagame_server(ip, port)

def run_client(ip, port):
    """
    Starts the Metagame client to connect to the specified server.

    Args:
        ip (str): IP address of the server to connect to.
        port (int): Port of the server to connect to.
    """
    start_metagame_client(ip, port)

def main():
    """
    Entry point of the application.
    Parses command-line arguments to determine whether to run as a server or client.
    """
    parser = ArgumentParser(description="A script that demonstrates using arguments.")

    parser.add_argument('ip', nargs='?', default=SERVER_DEFAULT_HOST, help='IP address for Metagame server to listen.')
    parser.add_argument('port', nargs='?', type=int, default=SERVER_DEFAULT_PORT, help='Port for Metagame server to listen.')
    parser.add_argument('-c', '--client', action='store_true', help='Start as client instead of server.')

    args = parser.parse_args()

    if args.client:
        run_client(args.ip, args.port)
    else:
        run_server(args.ip, args.port)

if __name__ == '__main__':
    main()