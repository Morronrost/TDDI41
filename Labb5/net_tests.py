import subprocess, socket

NETWORK = "10.0.0.0/24"
NETMASK = "10.0.0.255"
ROUTER_IP = "10.0.0.1"
HOSTNAME = open("/etc/hostname", "r").read().strip()

hosts = {
    "gw" : "10.0.0.1",
    "client-1" : "10.0.0.2",
    "client-2" : "10.0.0.3",
    "server" : "10.0.0.4"
}



def test_ip():
    result = subprocess.run("ip r", shell=True, stdout=subprocess.PIPE)
    resultDecoded = result.stdout.decode("utf-8").split()
    gateway = resultDecoded[2]

    if HOSTNAME != "gw":
        result = subprocess.run("ip addr | grep inet | grep ens3", shell=True, stdout=subprocess.PIPE)
    else:
        result = subprocess.run("ip addr | grep inet | grep ens4", shell=True, stdout=subprocess.PIPE)
    resultDecoded = result.stdout.decode("utf-8").split()

    netmask = resultDecoded[3]
    ip = resultDecoded[1]

    print("Gateway is: " + str(gateway))
    print("Netmask is: " + str(netmask))
    print("IP address is: " + str(ip))

    if HOSTNAME != "gw":
        assert gateway == ROUTER_IP
    assert netmask == NETMASK
    assert ip == hosts[HOSTNAME]+"/24"

def reach_ip(ip):
    result = subprocess.run(f"ping {ip} -c 1 | grep transmitted", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8").split()
    transmitted = result[0]
    recieved = result[3]
    assert transmitted == recieved == str(1)

def reach_gateway():
	if HOSTNAME != "gw":
		reach_ip(ROUTER_IP)
	else:
		reach_ip("10.0.0.2")

def test_ip_forwarding():
    result = subprocess.run("sysctl net.ipv4.ip_forward", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8").split()
    assert result[2] == "1"

def test_masquerade():
    result = subprocess.run("nft list ruleset | grep masquerade", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8").split()
    assert result[2] == "masquerade"

def test_firewall():
    result = subprocess.run("nc -zv localhost 22 | grep ssh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = result.stdout.decode("utf-8").split()

    assert result[-1] == "open"

    for host in hosts:
        reach_ip(hosts[host])
         

test_ip()
reach_gateway()
test_firewall()

if HOSTNAME == "gw":
    test_ip_forwarding()
    test_masquerade()