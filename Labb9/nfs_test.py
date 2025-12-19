import subprocess

HOSTNAME = open("/etc/hostname", "r").read().strip()

def test_export():
    result = subprocess.run("cat exportfs -v", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8")

    assert "/home" in result
    assert "/home-storage1" in result
    assert "/home-storage2" in result
    assert "10.0.0.2" in result
    assert "10.0.0.3" in result
    print(f"Server exports the following:\n {result}\n")

def test_on_boot():
    result = subprocess.run("cat /etc/fstab | grep 10.0.0.4", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8").split()[1]

    assert result == "/mnt/user_local"
    print(f"{result} is mounted to /usr/local and mounts on boot")

def test_rights():
    #Behöver inte?
    result = subprocess.run("exportfs -v", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8").split()[1][8:]

    print(f"")
    
def test_auto_master():
    result = subprocess.run("cat /etc/autofs.conf | grep master_map_name", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8")
    print(result)

    assert result == "master_map_name = ou=auto.master,ou=automount,dc=zorbak,dc=com"

if HOSTNAME == "server":
    test_export()

if HOSTNAME == "client-1" or HOSTNAME == "client-2":
    test_on_boot()
    test_auto_master()
