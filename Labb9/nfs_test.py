import subprocess

HOSTNAME = open("/etc/hostname", "r").read().strip()

def test_export():
    result = subprocess.run("exportfs -v", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8")

    print(f"Server exports the following:\n {result}\n")

def test_on_boot():
    result = subprocess.run("cat /etc/fstab | grep 10.0.0.4", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8").split()[1]

    assert result == "mnt/user_local"
    print(f"{result} is mounted to /usr/local and mounts on boot")

def test_rights():
    #Behöver inte?
    result = subprocess.run("exportfs -v", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8").split()[1][8:]

    print(f"")
    
def test_auto_master():
    