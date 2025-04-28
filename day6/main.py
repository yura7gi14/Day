import socket
import sys
import csv

input_file = sys.argv[1]
output_file = sys.argv[2]

results = []

with open(input_file, "r") as f:
    domains = f.read().splitlines()

for domain in domains:
    try:
        ip = socket.gethostbyname(domain)
        try:
            reverse = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            reverse = "-"
        results.append([domain, ip, reverse, "Success"])
    except socket.gaierror:
        results.append([domain, "-", "-", "Failed"])

# ここ "w"モードで開くのを忘れずに！
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["domain", "ip_address", "reverse_lookup", "status"])
    writer.writerows(results)
