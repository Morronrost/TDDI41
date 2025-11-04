import subprocess

DNS = "10.0.0.4"

def check_DNS():
    result = subprocess.run("cat /etc/resolv.conf", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8")

    assert DNS in result