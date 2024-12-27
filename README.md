# Metagames Project

## Overview
Metagames is a console-based application that simulates an in-game economy. The project consists of a server and client, enabling players to log in, manage their accounts, purchase and sell items, and view their balance and owned items.

### Components:
1. **Game Server**:
   - Manages user accounts, balances, and items.
   - Handles requests from clients for login, logout, buying, and selling items.
   - Stores data persistently using SQLite.

2. **Game Client**:
   - Provides a console interface for users to interact with the game server.
   - Allows users to log in, view their balance, manage items, and log out.

## Features
- **Account Management**:
  - Automatic account creation on first login.
  - Persistent storage of user data and items.

- **Item Transactions**:
  - Purchase items with in-game credits.
  - Sell owned items for a portion of their original cost.

- **Caching**:
  - Recently accessed accounts are cached for improved performance.

- **Networking**:
  - Server and client communicate using Python sockets.

## Requirements
- Python 3.7 or higher
- SQLite (pre-installed with Python)

### Python Packages
Required packages are listed in `requirements.txt`:
```
- pickle (standard library, no installation needed)
- threading (standard library, no installation needed)
```

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/wildluck/metagame
cd metagame
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.ps1   # Windows
```

If you encounter an execution policy error on Windows, run the following command in PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Then try activating the virtual environment again.


### 3. Install Dependencies
```bash
pip install -r requirements.txt # Optional
```

### 4. Initialize Database
Run the server to automatically initialize the SQLite database:
```bash
python metagame_server.py
```

## Usage

### Start the Server
```bash
python game_instance.py
```

### Start the Client
In a separate terminal:
```bash
python game_instance.py -c
```

Follow the on-screen prompts to log in, view your balance, and manage items.

## Directory Structure
```
Metagames/
├── game_instance.py          # Game entry point
├── metagame_server.py        # Game server implementation
├── metagame_client.py        # Game client implementation
├── custom_package/           # Custom enums and utilities
│   ├── custom_request.py     # Enum for request types
│   └── custom_status.py      # Enum for response statuses
├── game.db                   # SQLite database file (auto-created)
├── requirements.txt          # Python package dependencies (Optional, all imports need to installation)
├── venv/                     # Virtual environment directory
└── README.md                 # Project documentation)
```

## Example Commands

1. **Login:**
   - Enter a nickname to create or log in to an account.

2. **View Balance:**
   - Displays the current balance of in-game credits.

3. **Buy an Item:**
   - Choose an item to purchase if sufficient credits are available.

4. **Sell an Item:**
   - Sell owned items for a portion of their value.

## Contributing
Contributions are welcome! Fork the repository and submit a pull request.

## License
This project is licensed under the License. See `LICENSE` for more information.