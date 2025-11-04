## Virtuella maskiner: 'Guest' vs 'Host' - [QEMU.1] (https://www.ida.liu.se/~TDDI41/2025/uppgifter/qemu/index.sv.shtml#qemu.1)

    1. Vilken/vilka är gästmaskinerna?
        VM:en är gästmaskinen
    
    2. Vilken/vilka är värdmaskinerna?
	    Liu systemet är värdmaskinen

## Kopiera mellan gäst- och värdmaskiner - [QEMU.2] (https://www.ida.liu.se/~TDDI41/2025/uppgifter/qemu/index.sv.shtml#qemu.2)

    1. Kopiera filen /ect/network/interfaces från VM:en till er hemkatalog
	    scp /etc/network/interfaces ludka502@ssh.edu.liu.se:/home/ludka502

	2. Kopiera mappen /etc/default och allt dess innehåll från VM:en till er hemkatalog
	    scp -r /etc/default/ ludka502@ssh.edu.liu.se:/home/ludka502