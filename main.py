import re
import time
import os
import json

username = ""
kill_Msg = ""
death_Msg = ""
tf2Path = ""
currentClass = ""
ignoreClass = False

classKillMsg = {
    "scout": "",
    "soldier": "",
    "pyro": "",
    "demo": "",
    "heavy": "",
    "engineer": "",
    "medic": "",
    "sniper": "",
    "spy": ""
}

def configStartUp():
    global username
    global kill_Msg
    global death_Msg
    global tf2Path
    global classKillMsg
    global ignoreClass
    with open("./config.json", 'r') as f:
        config = json.load(f)
        username = config['username']
        kill_Msg = config['general_kill_msg']
        death_Msg = config['general_death_msg']
        tf2Path = config['tf2_path']
        ignoreClass = config['ignore_class']        
        if config['ignore_class'] == False:
            for cls in classKillMsg:
                key = f"{cls}_kill_msg"
                classKillMsg[cls] = config["class_Kill_msgs"].get(key, "")
        else:
            print("Ignore Class is True; Using General Messages.")
configStartUp()

def updateKillMsg(playerClass):
    global kill_Msg
    kill_Msg = classKillMsg[playerClass.lower()]

#   Files Paths
consoleOutputPath = f"{tf2Path}/console.txt"
dynamicKillCfgPath = f"{tf2Path}/cfg/DynamicKill.cfg"
dynamicDeathCfgPath = f"{tf2Path}/cfg/DynamicDeath.cfg"
lastkilled = ""
outputLines = []
kills = []
#   Stats
total_Kills = 0
total_Deaths = 0
queued = False

def extractData(console_msg):
    global lastkilled
    global total_Deaths
    global total_Kills
    global kills
    global outputLines
    global lastkilled
    global queued
    global ignoreClass

#   Commands
    if f"{username} connected" in console_msg:
        print("\n--Resetting; New Server Joined.\n")
        total_Deaths = 0
        total_Kills = 0
        kills.clear()
        outputLines.clear()
        lastkilled = ""

    if "Removed from match by system" in console_msg:
        print("\n--Leaving Server; Stats:")
        kd_ratio = total_Kills / total_Deaths if total_Deaths != 0 else total_Kills
        print(f"\nTotal Kills: {total_Kills}\nTotal Deaths: {total_Deaths}\nKD = {kd_ratio}")
        total_Deaths = 0
        total_Kills = 0
        kills.clear()
        outputLines.clear()
        lastkilled = ""

#   Dyamic Echo Cfg
    if "Dynamic Stats" in console_msg:
        kd_ratio = total_Kills / total_Deaths if total_Deaths != 0 else total_Kills
        print(f"\nTotal Kills: {total_Kills}\nTotal Deaths: {total_Deaths}\nKD = {kd_ratio}")

    if "Dynamic" in console_msg and (console_msg.split()[1] != "Stats"):
        print(f'You are now {console_msg.split()[1]}, Updating bind.')
        if ignoreClass != True:
            updateKillMsg(console_msg.split()[1])


    if "[PartyClient] Entering queue" in console_msg:
        print("\n--Entering Queue For New Server.")
        queued = True
    if "[PartyClient] Leaving queue" in console_msg:
        print("\n--Leaving Queue For New Server.")
        queued = False


#   Kill & Death Binds
    if "killed" not in console_msg:
        return "No one Killed"
    
    if username not in console_msg:
        return "Wrong person" 

    match = re.match(r"(.+?) killed (.+?) with", console_msg)
    if match:
        killerPlayer = match.group(1).strip()
        deadPlayer = match.group(2).strip()
        lastkilled = deadPlayer
        return killerPlayer, deadPlayer
    else:
        return "Wrong format."

if __name__ == "__main__":
    last_modified_time = 0
    while True:
        try:
#             Check if the file has been modified
            current_modified_time = os.path.getmtime(consoleOutputPath)
            if current_modified_time > last_modified_time:
                last_modified_time = current_modified_time

                with open(consoleOutputPath, 'r', encoding='utf-8', errors="ignore") as file:
                    lines = file.readlines()

                for line in lines:
                    outputLines.append(line)

#                 Process all new lines
                for line in outputLines:
                    result = extractData(line)
                    if isinstance(result, tuple) and result[1] != username:
                        if str(result) not in kills:
                            print(f"You Killed {lastkilled}")
                            kills.append(str(result))
                            lastkilled = result
                            total_Kills += 1

                            with open(dynamicKillCfgPath, 'w', encoding='utf-8', errors="ignore") as file:
                                file.write(f'say "{kill_Msg.format(str(result[1]))}"')
#                               print(f'say "{kill_Msg.format(str(result[1]))}")')

                    elif result[1] == username:
                        print(f"You died by {result[0]}")
                        total_Deaths += 1

                        with open(dynamicDeathCfgPath, 'w', encoding='utf-8', errors="ignore") as file:
                            file.write(f'say "{death_Msg.format(str(result[0]))}"')
#                           print(f'say "{death_Msg.format(str(result[0]))}")')

#                  Clear the file only after processing all new lines
                with open(consoleOutputPath, 'w', encoding='utf-8', errors="ignore") as file:
                    pass

                kills.clear()
                outputLines.clear()

        except FileNotFoundError:
            print("ERROR: File not found!")
            time.sleep(1)
            continue

        except Exception as e:
            print(f"ERROR: {e}")
            time.sleep(1)
            continue

        time.sleep(1)
