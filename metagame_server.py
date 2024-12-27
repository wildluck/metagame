"""
Metagames Project License

Copyright (c) 2024 Rishat Maksudov

Permission is granted to use, modify, and distribute this software for any purpose, with proper credit to the original author.

This software is provided "as is," without any warranty of any kind. The author is not responsible for any damages arising from its use.

"""


from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from random import randint
from custom_package.custom_request import RequestType
from custom_package.custom_status import ResponseStatus
from threading import Thread
from collections import OrderedDict
from sqlite3 import connect

# Constants for server configuration
DNOC = 50  # Default number of connections
NEW_ACCOUNT_CREDIT_MIN = 1500  # Minimum starting credits for new accounts
NEW_ACCOUNT_CREDIT_MAX = 2500  # Maximum starting credits for new accounts
MAX_CACHE_SIZE = 5  # Maximum number of accounts to cache
SELL_RATIO = 0.5  # Ratio of the item price refunded when selling
GAME_DB = 'game.db'  # Database file name

# Cache to store recently accessed accounts
account_cache = OrderedDict()

# Shop Items
SHIPS = {
    'Malta': 30000,
    'Black': 29500,
    'Marco Pole': 25000,
    'Pommern': 22000,
    'Scharnhorst': 18000,
    'Jager': 9200,
    'Anhalt': 5000,
    'Johan': 1500
}

PROJECTILES = {
    'AP': 600,  # Armor Piercing
    'HE': 500,  # High Explosive
    'SAP': 320,  # Semi Armor Piercing
    'DWT': 450,  # Deep Water Torpedos
    'AHT': 600,  # Acoustic Homing Torpedos
    'DC': 480,  # Depth Charges
    'DCA': 660  # Depth Charge Airstrike
}

SHOP_ITEMS = {**SHIPS, **PROJECTILES}

def init_db():
    """
    Initializes the SQLite database.
    Creates necessary tables if they do not exist.
    """
    conn = connect(GAME_DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                        nickname TEXT PRIMARY KEY,
                        credits INTEGER NOT NULL
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        nickname TEXT NOT NULL,
                        item_name TEXT NOT NULL,
                        FOREIGN KEY(nickname) REFERENCES accounts(nickname)
                      )''')
    conn.commit()
    conn.close()
    print("Database initialized.")

def handle_client(client_socket):
    """
    Handles communication with a single client.

    Args:
        client_socket (socket): The client socket connection.
    """
    conn = connect(GAME_DB)
    cursor = conn.cursor()

    def send_response(status, data):
        """
        Sends a response to the client.

        Args:
            status (ResponseStatus): The status of the response.
            data (dict): The data to include in the response.
        """
        client_socket.send(dumps({'response_status': status, 'response_data': data}))

    def update_cache(nickname, account_data):
        """
        Updates the cache with account data.

        Args:
            nickname (str): The nickname of the account.
            account_data (dict): The account data to cache.
        """
        account_cache[nickname] = account_data
        account_cache.move_to_end(nickname)
        if len(account_cache) > MAX_CACHE_SIZE:
            evicted = account_cache.popitem(last=False)
            print(f"Evicted {evicted[0]} from cache.")

    try:
        while True:
            request = loads(client_socket.recv(4096))
            request_type = request['request_type']
            request_data = request['request_data']

            if request_type == RequestType.LOG_IN:
                # Handle login request
                nickname = request_data['nickname']
                print(f"Processing login for {nickname}.")

                if nickname in account_cache:
                    account_data = account_cache[nickname]
                    print(f"Cache hit for {nickname}.")
                else:
                    cursor.execute('SELECT * FROM accounts WHERE nickname = ?', (nickname,))
                    account = cursor.fetchone()

                    if not account:
                        # Create a new account if it does not exist
                        starting_credits = randint(NEW_ACCOUNT_CREDIT_MIN, NEW_ACCOUNT_CREDIT_MAX)
                        cursor.execute('INSERT INTO accounts (nickname, credits) VALUES (?, ?)',
                                       (nickname, starting_credits))
                        conn.commit()
                        account = (nickname, starting_credits)
                        print(f"Created new account for {nickname} with {starting_credits} credits.")

                    cursor.execute('SELECT item_name FROM items WHERE nickname = ?', (nickname,))
                    owned_items = [row[0] for row in cursor.fetchall()]
                    account_data = {'nickname': account[0], 'credits': account[1], 'items': owned_items}

                    update_cache(nickname, account_data)

                send_response(ResponseStatus.SUCCESS, {'account': account_data, 'items': SHOP_ITEMS})

            elif request_type == RequestType.LOG_OUT:
                # Handle logout request
                send_response(ResponseStatus.SUCCESS, {'message': 'Logged out successfully.'})
                print("Client logged out.")
                break

            elif request_type == RequestType.GET_BALANCE:
                # Handle balance inquiry
                nickname = request_data['nickname']
                print(f"Fetching balance for {nickname}.")
                account_data = account_cache.get(nickname)

                if not account_data:
                    cursor.execute('SELECT credits FROM accounts WHERE nickname = ?', (nickname,))
                    credits = cursor.fetchone()[0]
                    account_data = {'nickname': nickname, 'credits': credits, 'items': []}
                    update_cache(nickname, account_data)

                send_response(ResponseStatus.SUCCESS, {'credits': account_data['credits']})

            elif request_type == RequestType.BUY_ITEM:
                # Handle item purchase
                nickname = request_data['nickname']
                item_name = request_data['item_name']

                cursor.execute('SELECT item_name FROM items WHERE nickname = ? AND item_name = ?', (nickname, item_name))
                if cursor.fetchone():
                    send_response(ResponseStatus.ERROR, {'message': 'Item already owned.'})
                else:
                    item_price = SHOP_ITEMS.get(item_name)
                    cursor.execute('SELECT credits FROM accounts WHERE nickname = ?', (nickname,))
                    credits = cursor.fetchone()[0]

                    if item_price and credits >= item_price:
                        # Deduct credits and add the item
                        new_credits = credits - item_price
                        cursor.execute('UPDATE accounts SET credits = ? WHERE nickname = ?', (new_credits, nickname))
                        cursor.execute('INSERT INTO items (nickname, item_name) VALUES (?, ?)', (nickname, item_name))
                        conn.commit()

                        account_cache[nickname]['credits'] = new_credits
                        account_cache[nickname]['items'].append(item_name)

                        send_response(ResponseStatus.SUCCESS, {'account': account_cache[nickname]})
                    else:
                        send_response(ResponseStatus.ERROR, {'message': 'Insufficient credits or invalid item.'})

            elif request_type == RequestType.SELL_ITEM:
                # Handle item sale
                nickname = request_data['nickname']
                item_name = request_data['item_name']

                cursor.execute('SELECT item_name FROM items WHERE nickname = ? AND item_name = ?', (nickname, item_name))
                if cursor.fetchone():
                    item_price = SHOP_ITEMS.get(item_name)
                    cursor.execute('SELECT credits FROM accounts WHERE nickname = ?', (nickname,))
                    credits = cursor.fetchone()[0]
                    new_credits = credits + int(item_price * SELL_RATIO)

                    cursor.execute('UPDATE accounts SET credits = ? WHERE nickname = ?', (new_credits, nickname))
                    cursor.execute('DELETE FROM items WHERE nickname = ? AND item_name = ?', (nickname, item_name))
                    conn.commit()

                    account_cache[nickname]['credits'] = new_credits
                    account_cache[nickname]['items'].remove(item_name)

                    send_response(ResponseStatus.SUCCESS, {'account': account_cache[nickname]})
                else:
                    send_response(ResponseStatus.ERROR, {'message': 'Item not owned.'})

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        conn.close()
        print("Client connection closed.")

def start_metagame_server(addr, port):
    """
    Starts the Metagame server.

    Args:
        addr (str): IP address of the server to bind to.
        port (int): Port number of the server to bind to.
    """
    init_db()
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((addr, port))
    server_socket.listen(DNOC)
    print(f"Server running on {addr}:{port}.")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected from {client_address}.")
            Thread(target=handle_client, args=(client_socket,)).start()
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        server_socket.close()
        print("Server socket closed.")