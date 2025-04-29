import ipaddress

cidr_input = input("IPアドレス/プレフィックスを入力して下さい(例:192.168.1.0/24) :")

network = ipaddress.ip_network(cidr_input, strict=False)

print(f"ネットワークアドレス: {network.network_address}")
print(f"ブロードキャストアドレス: {network.broadcast_address}")
print(f"使用可能ホスト数: {network.num_addresses - 2}")

hosts = list(network.hosts())
if hosts:
    print(f"ホスト範囲: {hosts[0]} ~ {hosts[-1]}")
else:
    print("使用可能なホストが存在しません")