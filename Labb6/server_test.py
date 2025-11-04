import subprocess

domain_name = "zorbak.com"

addresses = {
    "10.0.0.1" : "gw",
    "10.0.0.2" : "client-1",
    "10.0.0.3" : "client-2",
    "10.0.0.4" : "server"
}

def check_dns():
    result = subprocess.run("cat /etc/resolv.conf", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8").split()
    assert result[1] == "10.0.0.4" 

def check_config():
    result = subprocess.run("named-checkconf", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8")
    assert result == ""

def check_zone():
    fwd_result = subprocess.run(f"named-checkzone {domain_name} /etc/bind/db." + domain_name , shell=True, stdout=subprocess.PIPE)
    fwd_result = fwd_result.stdout.decode("utf-8")

    rev_result = subprocess.run(f"named-checkzone 0.0.10.in-addr.arpa /etc/bind/db.0.0.10", shell=True, stdout=subprocess.PIPE)
    rev_result = rev_result.stdout.decode("utf-8")
    
    assert "OK" in fwd_result
    assert "OK" in rev_result

def check_running():
    result = subprocess.run("systemctl list-units --type=service --state=running | grep named.service", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode("utf-8")

    assert "named.service" in result
    

def check_names():

    for address in addresses:
        fwd_result = subprocess.run(f"nslookup {addresses[address]}.{domain_name}", shell=True, stdout=subprocess.PIPE)
        fwd_result = fwd_result.stdout.decode("utf-8").split()
        
        assert fwd_result[-1] == f"{address}"

    for address in addresses:
        rev_result = subprocess.run(f"nslookup {address}", shell=True, stdout=subprocess.PIPE)
        rev_result = rev_result.stdout.decode("utf-8").split()

        assert rev_result[-1] == f"{addresses[address]}.{domain_name}."

check_dns()
check_config()
check_zone()
check_running()
check_names()