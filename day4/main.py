import socket

target = input("target:")
port_target_start = int(input("target port start:"))
port_target_end = int(input("target port finish:"))

for port in range(port_target_start, port_target_end + 1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target, port))

    if result == 0:
        print(f"Port {port} is OPEN")
    else:
        print(f"Port {port} is closed")
        
    sock.close()