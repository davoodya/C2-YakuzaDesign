
#----------Variables used in both Server and Client----------#
# C2 Server Port for client and Server
PORT = 80

# key use in Encryption/Decryption & This key must be 32 or fewer characters
KEY = "U can't touch this!"

#Path to use signifying a command request from a client using HTTP GET
CMD_REQUEST = "/book?isbn="

#Path to use signifying a command output from a client using HTTP GET
RESPONSE = "/inventory"

#Path to use signifying current directory from a client using HTTP GET
CWD_RESPONSE = "/title"


#Post variable name to user for assigning to command output from a client
RESPONSE_KEY = "index"


#----------Variables used in C2 server Only----------#
#Leave blank to Binding to all interfaces, Otherwise Enter C2 Servers IP Address
BIND_ADDR = ""

#Command to input timeout settings in seconds; 225 is right for Azure; set to None if unnecessary
#INPUT_TIMEOUT = 225
INPUT_TIMEOUT = None

"""Detect OS to Run below commands automatically to prevent against Azure, and other hosting environment 
from killing our Active Session,
[*] change KEEP_ALIVE_CMD value to command you want run to keep active session"""
KEEP_ALIVE_CMD = "whoami"

# KEEP_ALIVE_CMD based on OS
#
# from platform import system
#
# # set KEEP_ALIVE_CMD's value for Windows Builds only
# if system() == "Windows":
#     # get current time based on 24-hour clock(military time)
#     KEEP_ALIVE_CMD = "time /T"
#
# # set KEEP_ALIVE_CMD's value for Linux Builds only
# elif system() == "Linux":
#     # get current time based on 24-hour clock(military time)
#     KEEP_ALIVE_CMD = "date +%R" #Linux Builds
# # set KEEP_ALIVE_CMD's value on 'cd' for other Builds to prevent against timeout
# else:
#     KEEP_ALIVE_CMD = "cd"

# We should change User-Agent to avoid being blocked, But other keys is Optional
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/129.0.0.0 Safari/537.36"}



#----------Variables used in C2 Client Only----------#
# Set TOR Proxy to more secure and hide your IP address
# PROXY = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
PROXY = None

#C2 Server IP Address C2_SERVER = "127.0.0.1" 
C2_SERVER = "localhost" 

# Define sleep delay time in seconds for a reconnection attempt
DELAY = 3
