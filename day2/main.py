import subprocess

target = input()
response = subprocess.run(["ping", "-c", "1", target], capture_output=True, text=True)

if response.returncode == 0:
    print("Ping成功")
    print(response.stdout)
else:
    print("Ping失敗")