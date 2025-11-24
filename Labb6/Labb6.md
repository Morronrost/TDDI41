## Grunderna i DNS - [DNS.1](https://www.ida.liu.se/~TDDI41/2025/uppgifter/dns/index.sv.shtml#dns.1)

  ### 1. Vad är en auktoritativ namnserver?
    En auktoritativ namnserver som är utpekad eller vald av domänen för att ha ip-adressen lokalt sparad så att man       slipper leta upp den någon annanstans

     
  ### 3. Vad är alternativet till en auktoritativ namnserver
    De olika typerna av namnservrar utöver auktoritativ är rekursiv upplösare, root namnserver, TLD namnserver.
   
  ### 4. Är det skillnad mellan en domän och en zon? Vilken skillnad isåfall?
    Det finns skillnad mellan dem. En domän är ett logiskt namn i DNS hierarkin, medans en zon är en administrativ enhet som hanterar inställningarna inom en viss del av domännamnsrymden.
   
  ### 5. Vad innebär rekursiv slagning? Iterativ? Hur vet DNS-servern du frågar om det är en rekursivt ställd fråga?
      Rekursiv slagning inebär att DNS-servern själv hittar en ip-adress till domänen, medans en iterativ hänvisar till en annan DNS-server som kan ha informationen som söks. DNS-servern vet att det är en rekursiv fråga genom att sätta en flagga i DNS-förfrågan.
   
  ### 6. I DNS delegerar vi ansvaret för olika zoner. Varför?
      DNS delegeras i olika zoner för att göra den mer skalbar och lättare att hantera.
   
  ### 7. Ovan beskriver vi hur man kommer fram till att liu.se har adressen 130.236.18.52 (och hela delegerings-hierarkin från root till auktoriteten för .se-domänen, till liu.se). Hur sker en uppslagning ''åt andra hållet'', där man vill slå upp om adressen 130.236.18.52 motsvarar någon webbadress (enligt din DNS-server)? Du kan vilja läsa om reverse DNS.
      Omvänd DNS-förfrågan fungerar genom att gå igenom DNS-serverns ptr(pointer) register och hitta domänen som hör till ip-adressen.



## dig - [DNS.2](https://www.ida.liu.se/~TDDI41/2025/uppgifter/dns/index.sv.shtml#dns.2)

  ### 1. Förklara kortfattat vad de olika delarna av utskriften innebär.
      Den första raden berättar vilken version av "dig" som körs. 
      Header delen summerar DNS-förfrågan, den berättar frågetypen, respons statusen och flaggor som till exempel rekursiv flaggan. Den listar också ut frågor, svar, auktoritativa- och ytterligare uppgifter i DNS-svaret.
      I "Pseudosection" visas det om en förlängning på DNS är använt, den specifierar vilka flaggor som används och storleken på udp paketet.
      I "Question" så visas domännamnet som förfrågas, att frågan är över internet och att svaret är en adress record
      Answer visar svaren på frågorna från question, fast det finns också en Time to Live timer och ip-adressen som domänen är kopplad till
      Längst ner visas hur snabbt svaret kom, DNS-serverns ip-adress och port, när dig kommandot kördes och storleken på DNS-serverns svar.
     
  ### 2. När du gör en query som till exempel dig ANY liu.se @ns4.liu.se kan du få flera olika sorters resource records (RR) tillbaka. Vad ska A-, AAAA-, NS-, MX- och SOA-records innehålla?
      A-records är en Adress record och tilldelar ett domännamn till en IPv4 adress, och innehåller domännamn och IP-adressen
      AAAA-records är en Adress record som tilldelar domännamnen till en IPv6 adress, innehållersmma som A-records
      NS-records är en Name Server record och specifierar den auktoritativa nameserver för en domän. Denna innehåller domännamnet och en kvalifierad FQDN av den namnservern
      MX-records är en Mail Exchange record och dirigerar epost till servrar som kan ta hand om dom. Dessa innehåller domännamnet, en proritet till varje mejlserver och FQDN för mejlservern
      SOA-records är en Start of Authority record och innehåller administrativ information om DNS-zonen. Den innehåller FQDN av den primära auktoritativanamnservern, emejladressen till administratorn för zonen, serialnummer till zonfilen, Refresh-, Retry- och Expire intervaller och minimum TTL.
  
  ### 3. Kör dig +trace www.google.com och förklara kortfattat vad som står.
      Den startar med att fråga root DNS servrar för att hitta auktoritativen till .com TLD:n. Sedan frågas TLD:n efter auktoritativen till google.com, när den har hittats så frågas googles auktoritativanamnserver efter googles ip-adress. Sist så visas det A-record som retuneras av googles egna DNS

## Konfiguration av namnserver - [DNS.3](https://www.ida.liu.se/~TDDI41/2025/uppgifter/dns/index.sv.shtml#dns.3)

  ### 1. Hur sätter man önskad DNS-server på Linux
      Öppna /etc/resolv.conf och lägg till: nameserver "DNS-IP".
  
  ### 2. Vad är en SOA post? Vad innebär dess olika fält?
      SOA står för "start of authority". 
      MMNAME:  namnet på namnservern.
      SERIAL:  serialnummer.
      REFRESH: tiden (i sekunder) som sekundärservrarna ska vänta förrens de checkar med primärservern om SOA posten ska uppdateras.
      RETRY:   tiden en server ska vänta på en icke responsiv primärservern förrens den frågar servern igen.
      EXPIRE:  är tiden som sekundärservrarna ska vänta på svar från primärservern förrens de slutar svara på förfrågningar angående zonen.
  ### Motivering
    Vi döpte zonen/domänen till Zorbak. För SOA så utgick vi från db.local, det som vi ändrade på i den var domännamnet, och serialnummret till dagens datum med ett nummer i slutet som ökade för varje uppdatering.
    För reverse filen använde vi istället db.0 som vår mall och ändrade samma saker som i forward-dns filen.
    Anledningen vi valde att använda servern som DNS är för att routern används som gateway och för att vi inte vill att klienter ska kunna komma åt och ändra i DNS:en.


## Testning av DNS-konfiguration - [DNS.4](https://www.ida.liu.se/~TDDI41/2025/uppgifter/dns/index.sv.shtml#dns.4)

  Client:
  
    import subprocess
  
    DNS = "10.0.0.4"
  
    def check_DNS():
        result = subprocess.run("cat /etc/resolv.conf", shell=True, stdout=subprocess.PIPE)
        result = result.stdout.decode("utf-8")
    
        assert DNS in result

  Server:

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


