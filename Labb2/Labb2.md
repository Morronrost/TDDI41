## Introduktion till man - [LXB.1](https://www.ida.liu.se/~TDDI41/2025/uppgifter/lxb/index.sv.shtml#lxb.1)

    1. Vilka är de 9 avsnitten?
       	1   Executable programs or shell commands
       	2   System calls (functions provided by the kernel)
       	3   Library calls (functions within program libraries)
       	4   Special files (usually found in /dev)
       	5   File formats and conventions, e.g. /etc/passwd
       	6   Games
       	7   Miscellaneous  (including  macro  packages  and  conventions),  e.g. man(7), groff(7), man-pages(7)
       	8   System administration commands (usually only for root)
       	9   Kernel routines [Non standard]
    
    2. Vilket avsnitt dokumenterar kommandoradsverktyg så som cat eller ls?
        Avsnitt 1.

## Introduktion till rör - [LXB.2](https://www.ida.liu.se/~TDDI41/2025/uppgifter/lxb/index.sv.shtml#lxb.2)

    1. Kör journalctl, och med hjälp av tail visa bara de sista 5 raderna.
        journalctl | tail -n 5

## Justering av filrättigheter - [LXB.3](https://www.ida.liu.se/~TDDI41/2025/uppgifter/lxb/index.sv.shtml#lxb.3)

    1. Hur byter man ägare på en fil?
        chown "USER" "FILE"

    2. Hur gör man en fil körbar enbart för dess grupp?
        chmod g+x "FILE"

## Arkivering och komprimering med tarballs - [LXB.4](https://www.ida.liu.se/~TDDI41/2025/uppgifter/lxb/index.sv.shtml#lxb.4)

    1. Hur packar man upp en .tar.gz fil?
        tar -xf "FILE"

    2. Hur packar man ner en mapp i en .tar.xz fil?
        tar -cJf "FILENAME.tar.xz" "DIRECTORY TO COMPRESS"

## Miljövariabler - [LXB.5](https://www.ida.liu.se/~TDDI41/2025/uppgifter/lxb/index.sv.shtml#lxb.5)

    Vi testade echo, sedan så använde vi export PATH="DIRECTORY PATH" för att lägga courses/TDDI41 i vår path. 
    Efter det så använde vi vim och redigerade .bashrc för att permanent lägga till /courses/TDDI41/ i path genom att lägga in PATH= kommandot i filen. 
    Vi ändrade LC_ALL med export kommandot och det gjorde man till svenska.


## Introduktion till systemd - [LXB.6](https://www.ida.liu.se/~TDDI41/2025/uppgifter/lxb/index.sv.shtml#lxb.6)
    
    1. Hur får man en lista över alla systemd-enheter (units)?
        Man använder kommandot systemctl, kan även pipe:a kommandot grep för att endast få upp systemd

    2. Hur startar man om sin ssh-server (starta systemtjänsten)?
        Man kör kommandot /etc/init.d/ssh restart

## Systemloggar - [LXB.7](https://www.ida.liu.se/~TDDI41/2025/uppgifter/lxb/index.sv.shtml#lxb.7)

    journalctl | grep sshd
    Sep 17 08:57:02 debian sshd[542]: pam_unix(sshd:session): session opened for user root(uid=0) by (uid=0)

## SSH-nycklar för autentisering - [LXB.8](https://www.ida.liu.se/~TDDI41/2025/uppgifter/lxb/index.sv.shtml#lxb.8)

    1. Kommandot för att skapa en nyckel
		ssh-keygen -t ecdsa

    2. Nyckelfilen
		id-sysadminkurs-ed25519.pub

    3. ssh-add -l
		256 SHA256:XFN864C/0wabqiPuhQ06PHygfJedeVk9WSsRG6gz64o ludka502@su15-211.ad.liu.se (ECDSA)