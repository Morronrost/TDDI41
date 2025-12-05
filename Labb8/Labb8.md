## Grunderna i NTP - [NTP.1](https://www.ida.liu.se/~TDDI41/2025/uppgifter/ntp/index.sv.shtml#ntp.1)
  ### 1. Varför NTP är stratifierat (har strata, som på engelska heter stratum)? Varför talar man inte bara direkt med någon referensserver?
      Flera anledningar, en är t.ex redundancy, om en referensserver är nere så kan resten ändå hålla en korrekt tid. Flera servrar delar även ut bördan så att en server inte blir överfull med requests.
    
  ### 2. En NTP-klient brukar inte bara ändra systemklockan till en viss tid direkt, utan ökar/minskar hastigheten så att man når målet lite mjukare. Varför?
      En stor tidsförändring kan förvirra system och orsaka problem, medans om man bara ökar/sänker hastigheten så blir det inget oväntat beteende.
    
  ### 3. Installera paketet ntp på er router. Kör ntpq -p och förklara vad de olika kolumnerna betyder, och hur man ska tolka att det finns flera rader i tabellen. Ta med utdata från kommandot.
      Remote är routerns konfigurerade NTP servrar.
      Refid är vart NTP servrarna är syncade 
      st är vilket stratum servern är på
      t är vilken typ av synkronitisering som server gör
      when är tiden sedan senast lyckade meddelande till servern
      poll är polling intervallet
      reach är ett 8-bit shift register som visar statusen på de 8 senaste meddelanden.
      delay är total round trip time
      offset är tidsskillnaden i ms mellan servern och routern
      jitter är den estimerade errorn i ms.

## Konfiguration av NTP - [NTP.2](https://www.ida.liu.se/~TDDI41/2025/uppgifter/ntp/index.sv.shtml#ntp.2)
  ### Hur ser man på detta utdata att er output i någon mening är vettig relativt kraven? 
      I remote ser vi att den går mot routern och den är markerad med *, vilket betyder att den är syncad.
      Vi ser inte heller någon annan server när vi kör ntpq -p.
      Vi kan också se att vår stratum är 2 på klienterna, vilket stämmer då vi är 2 ifrån referensen.

  ### Utdata för router
      *192.36.143.134  .PPS.    1  u  61  64  377  3.969  +3.777  3.849
  ### Utdata för klient
      *gw.zorbak.com  192.36.143.134  2  u  21  64  1  1.668  +2.932  1.248
      
## Testning av NTP-konfiguration - [NTP.3](https://www.ida.liu.se/~TDDI41/2025/uppgifter/ntp/index.sv.shtml#ntp.3)
    import subprocess
    
    HOSTNAME = open("/etc/hostname", "r").read().strip()
    
    def test_config():
    	result = subprocess.run("cat /etc/ntp.conf | grep iburst", shell=True, stdout=subprocess.PIPE)
    	result = result.stdout.decode("utf-8").split()
    	print(result[1])
    
    	if HOSTNAME != "gw":
    		assert result[1] == "10.0.0.1"
    	else:
    		assert result[1] == "se.pool.ntp.org"
    
    def test_queries():
    	result = subprocess.run("ntpq -p | grep '*' ", shell=True, stdout=subprocess.PIPE)
    	result = result.stdout.decode("utf-8").split()
    
    	print(result[0])
    	if HOSTNAME != "gw":
    		assert result[0] == "*gw.zorbak.com"
    	else:
    		assert result[0][0] == "*"
    
    
    	print(result[-2])
    	assert float(result[-2]) < 1.5 and float(result[-2]) > -1.5
    
    test_queries()
    test_config()
    

