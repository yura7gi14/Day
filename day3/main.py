import subprocess
import ipaddress

ip_addr = input("ip address:")

net = ipaddress.ip_network(ip_addr)
ips = [str(ip) for ip in net.hosts()]

for ip in ips:
    print(f"{ip}にping中...")

    response = subprocess.run(
        ["ping", "-c", "1", "-W", "1", ip],
        capture_output=True,
        text=True
    )

    if response.returncode == 0:
        print(f"{ip}は生存している\n")
    else:
        print(f"{ip}は応答なし")