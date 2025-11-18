## ping - [NET.1](https://www.ida.liu.se/~TDDI41/2025/uppgifter/net/index.sv.shtml#net.1)
  1. Vad är kommandot för att skicka fem paket till localhost?
     ping -c 5 localhost
     
  3. Vad är kommandot för att skicka tre paket till localhost med två sekunders mellanrum mellan varje paket?
     ping -c 3 -i 2 localhost


## ip - [NET.2](https://www.ida.liu.se/~TDDI41/2025/uppgifter/net/index.sv.shtml#net.2)
  1. Vad är kommandot för att lista adresserna för alla nätverksinterface i datorn?
     ip addr
     
  3. Vad är kommandot för att ta nätverksinterfacet ens4 online?
     ip link set ens4 up
     
  5. Vad är kommandot för att ge nätverksinterfacet ens4 ip-adressen 192.168.1.2 med en 24-bitars nätmask?
     ip addr add 192.168.1.2/24 dev ens4
     
  7. Vad är kommandot för att visa routing-tabellen?
     route



## Nätverkskonfiguration - [NET.3](https://www.ida.liu.se/~TDDI41/2025/uppgifter/net/index.sv.shtml#net.3)
  För att konfigurera ipadresser, nätmasker och gateways gick vi in i /etc/network/interfaces filen och konfigurerade nätverksadaptern enligt följande:
  
    address 10.0.0.X (X är 1 för router, 2 för klient1, 3 för klient2 och 4 för servern)
    netmask 255.255.255.0
    gateway 10.0.0.1(routerns ip)

## IP-forwarding och -masquerading - [NET.4](https://www.ida.liu.se/~TDDI41/2025/uppgifter/net/index.sv.shtml#net.4)
  Vi satte igång ip-forwarding i sysctl.conf samt satte följande inställningar i nftables.conf:
  
    table ip nat {
    	chain prerouting {
    	  type nat hook prerouting priority dstnat; policy accept;
    	 }
    
      chain postrouting {
    	  type nat hook postrouting priority -100; policy accept;
    		oifname "ens3" masquerade
  	}


## Justering av värdnamn - [NET.5](https://www.ida.liu.se/~TDDI41/2025/uppgifter/net/index.sv.shtml#net.5)
  Värdnamnen sattes i /etc/hostname och /etc/hosts samt FQDN i /etc/hosts enligt instruktion.

## Brandväggar med nftables - [NET.6](https://www.ida.liu.se/~TDDI41/2025/uppgifter/net/index.sv.shtml#net.6)

    table inet filter {
  	  chain inbound {
    		#by default drop all trafic unless it meets filter criteria
    		type filter hook input priority 0; policy drop;
        
        #allow traffic from established and related packets, drops invalid
        ct state vmap { established: accept, related: accept, invalid: drop }
    
    		#accepts loopback traffic
    		iifname lo accept
    
    		#allow SSH on port TCP/22 and dns on UDP/53
    		tcp dport { 22 } accept
    		udp dport { 53 } accept
    
    		#accept ping requests
    		icmp type echo-request accept
    
    		#accepts neighbor discovery or connectivity breakes
    		icmpv6 type { nd-neighbor-solicit, nd-router-advert, nd-neighbor-advert } accept
    	}
    }

## Testning av nätverkskonfiguration - [NET.7](https://www.ida.liu.se/~TDDI41/2025/uppgifter/net/index.sv.shtml#net.7)
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

