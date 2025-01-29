import re
import time
import os


username = ""
kill_Msg = "You are dead {}" #  The "{}" are were the username is going to be printed
death_Msg = "nice {}"
tf2Path = "C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf"


#   Files Paths
consoleOutputPath = f"{tf2Path}/console.txt"
DynamicKillCfgPath = f"{tf2Path}/cfg/DynamicKill.cfg"
DynamicDeathCfgPath = f"{tf2Path}/cfg/DynamicDeath.cfg"

lastkilled = ""
outputLines = []
kills = []

#   Stats
total_Kills = 0
total_Deaths = 0
queued = False

def extract_data(console_msg):

    global lastkilled
    global total_Deaths
    global total_Kills
    global kills
    global outputLines
    global lastkilled
    global queued

#   Commands
    if f"{username} connected" in console_msg:
        print("\n--Resetting; New Server Joined\n")
        total_Deaths = 0
        total_Kills = 0
        kills.clear()
        outputLines.clear()
        lastkilled = ""

    if "Removed from match by system" in console_msg:
        print("\n--Leaving Server; Printing Stats:")
        kd_ratio = total_Kills / total_Deaths if total_Deaths != 0 else total_Kills
        print(f"\nTotal Kills: {total_Kills}\nTotal Deaths: {total_Deaths}\nKD = {kd_ratio}")
        total_Deaths = 0
        total_Kills = 0
        kills.clear()
        outputLines.clear()
        lastkilled = ""


    if "Dynamic Stats" in console_msg:
        kd_ratio = total_Kills / total_Deaths if total_Deaths != 0 else total_Kills
        print(f"\nTotal Kills: {total_Kills}\nTotal Deaths: {total_Deaths}\nKD = {kd_ratio}")
    
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
                    result = extract_data(line)
                    if isinstance(result, tuple) and result[1] != username:
                        if str(result) not in kills:
                            print(f"You Killed {lastkilled}")
                            kills.append(str(result))
                            lastkilled = result
                            total_Kills += 1

                            with open(DynamicKillCfgPath, 'w', encoding='utf-8', errors="ignore") as file:
                                file.write(f'say "{kill_Msg.format(str(result[1]))}"')
#                               print(f'say "{kill_Msg.format(str(result[1]))}")')

                    elif result[1] == username:
                        print(f"You died by {result[0]}")
                        total_Deaths += 1

                        with open(DynamicDeathCfgPath, 'w', encoding='utf-8', errors="ignore") as file:
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
