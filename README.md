# Dynamic Binds for Team Fortress 2

This Project allows for binds to change dynamically, In this example it makes two binds, 1 for when you die and 1 for when you kill somone. 

## Setup

### Prerequisites

- At least Python 3.10 installed on your system.
- regular expressions installed.
- Team Fortress 2 installed.

### Installation

1. Clone the repository to your local machine or download the files:

    ```sh
    git clone https://github.com/kisstopherr/Dynamic-Binds.git
    cd Dynamic-Binds
    ```
2. Install regular expressions or `re`:

   ```sh
   pip install re
   ```

4. Create an `autoexec.cfg` file in your TF2 game directory (C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\cfg) with the following content:
   
    ```cfg
    con_logfile console.txt
    con_timestamp 0
    bind F4 "exec DynamicDeath.cfg"
    bind F7 "exec DynamicKill.cfg
    bind F1 "echo Dynamic Stats"
    ``` 

5. Create an `DynamicDeath.cfg` and `DynamicKill.cfg` file in your TF2 game directory (C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\cfg) and leave it blank, as it will always be changing.

NOTE:

- Customize the bind keys, `F4`, `F7`, `F1` to suit your preferences.
- `F1` will print your stats (K/D Ratio) in the console. (IT DOES NOT RESET AFTER PRE-GAME) 

### Setup

- Edit the `main.py` file, and to set the `username`, `tf2Path`, `kill_Msg`, and `death_Msg` variables as needed.

    ```python
    username = "YOUR USERNAME"
    kill_Msg = "You are dead {}" #  The "{}" are were the username is going to be printed
    death_Msg = "nice {}"
    tf2Path = "C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf"
    ```
    
NOTE:

- The players name will replace the `{}` in your messages.


## Usage

1. Run the bot:

    ```sh
    python main.py
    ```

2. The bot continuously monitors the `console.txt` file for relevant events:
    - When you kill someone, the `DynamicKill.cfg` file will be updated with your personalized `kill_Msg`.
    - When someone kills you, the `DynamicDeath.cfg` file will be updated with your personalized `death_Msg`.

3. Keep the bot running while playing Team Fortress 2 to enjoy dynamic binds!

# How it works

1. **Console Monitoring**:
    - The bot reads `console.txt`, the game’s log file, every second.
    - It extracts relevant data such as kills, deaths, and game events using regular expressions.

2. **Dynamic Binds**:
    - When you kill a player:
        - Their username replaces `{}` in the `kill_Msg`.
        - This message is written to `DynamicKill.cfg`.
    - When another player kills you:
        - Their username replaces `{}` in the `death_Msg`.
        - This message is written to `DynamicDeath.cfg`.

3. **Real-time Updates**:
    - The bot uses `time.sleep(1)` to continuously scan for new events in the log and update the configuration files.

4. **Stats Tracking**:
    - Tracks total kills, deaths, and calculates a Kill/Death (K/D) ratio.
    - Displays stats in the console when specific events occur (e.g., joining or leaving a server).


