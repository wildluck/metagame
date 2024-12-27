"""
Metagames Project License

Copyright (c) 2024 Rishat Maksudov

Permission is granted to use, modify, and distribute this software for any purpose, with proper credit to the original author.

This software is provided "as is," without any warranty of any kind. The author is not responsible for any damages arising from its use.

"""


from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from custom_package.custom_request import RequestType
from custom_package.custom_status import ResponseStatus

def tx_request(client_socket, request_type: RequestType, request_data):
    """
    Sends a request to the server and receives the response.

    Args:
        client_socket (socket): The socket connection to the server.
        request_type (RequestType): The type of request to send.
        request_data (dict): The data to include in the request.

    Returns:
        dict: The server's response.
    """
    client_socket.send(dumps({'request_type': request_type, 'request_data': request_data}))
    return loads(client_socket.recv(4096))

def display_main_menu():
    """
    Displays the main menu options for the user.
    """
    print("\nMain Menu")
    print("1 - Show Balance")
    print("2 - Show Available Items")
    print("3 - Show Owned Items")
    print("4 - Buy an Item")
    print("5 - Sell an Item")
    print("6 - Logout")

def handle_menu_option(client_socket, nickname, items, account):
    """
    Handles the user's menu selection and performs corresponding actions.

    Args:
        client_socket (socket): The socket connection to the server.
        nickname (str): The user's nickname.
        items (dict): The available items in the game.
        account (dict): The user's account information.

    Returns:
        bool: True if the client should continue, False if the client wants to log out.
    """
    option = input("Select an option: ")

    if option == '1':
        response = tx_request(client_socket, RequestType.GET_BALANCE, {'nickname': nickname})
        print(f"Your current balance is: {response['response_data']['credits']} credits.")
    elif option == '2':
        print("Available items for purchase:")
        for name, price in items.items():
            print(f"{name} - {price} credits")
    elif option == '3':
        print("Items you own:")
        for item in account['items']:
            print(f"- {item}")
    elif option == '4':
        item_name = input("Enter the name of the item to buy: ")
        response = tx_request(client_socket, RequestType.BUY_ITEM, {'nickname': nickname, 'item_name': item_name})
        if response['response_status'] == ResponseStatus.ERROR:
            print(f"Error: {response['response_data']['message']}")
        else:
            account.update(response['response_data']['account'])
            print(f"You have successfully purchased {item_name}.")
    elif option == '5':
        item_name = input("Enter the name of the item to sell: ")
        response = tx_request(client_socket, RequestType.SELL_ITEM, {'nickname': nickname, 'item_name': item_name})
        if response['response_status'] == ResponseStatus.ERROR:
            print(f"Error: {response['response_data']['message']}")
        else:
            account.update(response['response_data']['account'])
            print(f"You have successfully sold {item_name}.")
    elif option == '6':
        tx_request(client_socket, RequestType.LOG_OUT, {})
        print("You have logged out. Goodbye!")
        return False
    else:
        print("Invalid option. Please try again.")
    return True

def start_metagame_client(addr, port):
    """
    Starts the Metagame client and connects to the server.

    Args:
        addr (str): IP address of the server.
        port (int): Port number of the server.
    """
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((addr, port))

    try:
        nickname = input("Enter your nickname: ")
        response = tx_request(client_socket, RequestType.LOG_IN, {'nickname': nickname})

        if response.get('response_status') == ResponseStatus.SUCCESS:
            response_data = response['response_data']
            account = response_data['account']
            items = response_data['items']

            print(f"Welcome, {nickname}! You have successfully logged in.")
            print(f"Your starting balance: {account['credits']} credits.")

            while True:
                display_main_menu()
                if not handle_menu_option(client_socket, nickname, items, account):
                    break
        else:
            print(f"Login failed for {nickname}. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Disconnected from the server.")