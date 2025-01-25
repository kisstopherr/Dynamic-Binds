# Dynamic Binds for Team Fortress 2

This Project is allows for binds to change dynamically, In this examples it makes two binds, 1 for when you die and 1 for when you kill somone. 

## Setup

### Prerequisites

- At least Python 3.10 installed on your system.
- Team Fortress 2 installed.

### Installation

1. Clone the repository to your local machine or download the files:

    ```sh
    git clone https://github.com/kisstopherr/Dynamic-Binds.git
    cd Dynamic-Binds
    ```

2. Create an `autoexec.cfg` file in your TF2 game directory (C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\cfg) with the following content:
   
    ```cfg
    developer 1
    con_logfile console.txt
    con_timestamp 0
    bind F4 exec DynamicDeath.cfg
    bind F7 exec DynamicKill.cfg
    ``` 

4. Create an `DynamicDeath.cfg` and `DynamicKill,cfg` file in your TF2 game directory (C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\cfg) and leave it blank, as it will always be changing.

NOTE:

- You can change the `F4` and `F7` to any button you want for your binds

### Setup

- Edit the `main.py` file, and to set the `username` and `log_file` and both Messages variables as needed.

    ```python
    username = "your name"
    log_file = "C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf/console_chatlog.txt"
    deathMsg = "Nice"
    KillMsg = "You are now dead"
    ```
    
NOTE:

- The players name will be added to the end of the messages.


## Usage

1. Run the bot:

    ```sh
    python main.py
    ```

2. The bot will read the chat log every second and change the binds to whom ever killed your or you killed.

3. Then you're done, leave the file running and you will get Dynamic Binds. 
