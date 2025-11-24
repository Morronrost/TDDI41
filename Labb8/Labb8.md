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


## Testning av NTP-konfiguration - [NTP.3](https://www.ida.liu.se/~TDDI41/2025/uppgifter/ntp/index.sv.shtml#ntp.3)

