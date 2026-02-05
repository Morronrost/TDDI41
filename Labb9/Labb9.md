## Kommando för filsystem - [STO.1](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.1)
  ### 1. Vad är syftet med /etc/fstab?
    Fstab är en konfigurationsfil som används för att bestäma vart filsystemen och partitioner blir automatiskt monterade vid uppstart.
  
  ### 2. Vad används kommandot mke2fs (mkfs.ext{2..4}) till?
    Kommandot används för att skapa ett filsystem av typen ext{2..4} på en partition.
  
  ### 3. Vad skriver kommandot df -h ut?
    Kommandot skriver ut hur mycket ledig plats det finns på varje partition, -h flaggan skriver ut dom i Kilo-, Mega-, Giga- etc. format
  
  ### 4. Förklara vad kommandot mount -t ext3 /dev/sdb2 /mnt/media innebär.
    Det betyder att man monterar en ext3 partition som ligger på /dev/sdb2 till /mnt/media/ 
  
## RAID - [STO.2](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.2)
  ### 1. Vad står förkortningen RAID för?
    Det står för Redundant Array of Independant Disks
  
  ### 2. Förklara i grova drag hur RAID-0 fungerar
    Den skriver/läser varannan block från hårddiskarna, t.ex block 1 från hdd 1, block 2 från hdd 2, block 3 från hdd 1 osv...
    Detta resulterar i högre hastighet då båda diskarna kan skriva samtidigt.
  
  ### 3. Förklara i grova drag hur RAID-1 fungerar
    RAID-1 betyder att disken kopieras exakt till en annan disk för att ha parity/backup ifall den första disken felar.
  
  ### 4. Vad innebär kommandot mdadm --stop /dev/md0 ?
    Det stänger av arrayen på /dev/md0
    
## (Av)montera diskar - [STO.3](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.3)
    Börja med kommandot mdadm --create /dev/md0 --levels=1 --raid-devices=2 /dev/vda /dev/vdb
    Formatera sedan raid1 partitionen till ext4 med mke2fs -t ext4 /dev/md0
    Montera partitionen med mount -t ext4 /dev/md0 /mnt
    Verifiera med df -T
    Avmontera partitionen med umount /dev/md0

    RAID 0:
    mdadm --create /dev/md1 --levels=0 --raid-devices=2 /dev/vdc /dev/vdd
    Formatera med ext4 med mke2fs -t ext4 /dev/md1
    Montera partitionen med mount -t ext4 /dev/md1 /mnt
    Verifiera med df -T
    Avmontera partitionen med umount /dev/md1
    
## LVM - [STO.4](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.4)
  ### 1. Förklara följande begrepp: Fysisk volym (PV: Physical Volume), volymgrupp (VG: Volume Group) och logisk volym (LV: Logical Volume) och hur de hänger ihop.
    Fysisk volym är partioner eller diskar som inte är formaterade, volym grupper är en samling av fysiska volymer och logiska volymer är virtuella partitioner. 
    När de fysiska volymerna är grupperade i volymgrupper så kan man skapa en logisk volym som ses som bara en partition. T.ex 2 diskar på 500GB vardera kan se ut som en disk på 1TB.
  
  ### 2. Vad är kommandot för att göra klart en fysisk volym för LVM?
    För att skapa en fysisk volym används kommandot pvcreate [partition]
  
  ### 3. Vad är kommandot för att skapa en volymgrupp?
    Volymgrupper skapas av kommandot vgcreate [namn på grupp] [partition]
  
  ### 4. Vad är kommandot för att utöka en volymgrupp med ytterligare en PV?
    vgextend [namn på grupp] [fysiska partition]
  
  ### 5. Hur skapar du en logisk volym på 100MiB från en volymgrupp?
    lvcreate --name [namn på volym] --size 100m [namn på grupp]

## Hantering av volymer och volymgrupper - [STO.5](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.5)
    Skapade fysiska volymer med kommandona pvcreate /dev/md0 och pvcreate /dev/md1 för att initialisera inför LVM
    Skapade en volymgrupp med vgcreate vgvirt /dev/md0 och utökade den med vgextend vgvirt /dev/md1
    Skapade logiska volymer med lvcreate --name lvvol1/lvvol2 --size 100m vgvirt
    Formaterade till ext4 med mke2fs -t ext4 /dev/vgvirt/lvvol{1..2}
    Monterade vid boot genom att redigera /etc/fstab:
    /dev/vgvirt/lvvol{1..2} /home-storage{1..2} ext4 defaults 0 2
    
## Konfigurering av NFS - [STO.6](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.6)
    Laddade ner nödvändiga paket med apt install nfs-kernel-server
    Redigerade i /etc/default/nfs-common, satte NEED_STATD=no och NEED_IDMAPD=yes
    Redigerade i /etc/default/nfs-kernel-server, satte RPCNFSDOPTS="-N 2 -N 3" och RPCMOUNTDOPTS="--manage-gids -N 2 -N3". Detta för att stänga av nfs v2 och v3
    Skapade en mapp /srv/nfs4, la till -p flaggan som skapar parent mappar om nödvändigt. Sedan skapades en symbolisk länk mellan /usr/local och /srv/nfs4/usr_local med ln kommandot.
    Redigerade i /etc/exports, avkommenterade /srv/nfs4 delen. fsid=0 berättar att psuedo-root är toppen, no_subtree_check berättar att den inte ska check inodes.
    Ändrade i nftables.conf, tillåt tcp port 2049 genom brandväggen (standard port för nfs)

  ### På klienten
    Laddade ner nfs-common
    Skapade en mapp /mnt/user_local och sedan monterade /usr/local från servern till den med kommandot "mount -t nfs4 10.0.0.4:/ /mnt/user_local"
    Redigerade i /etc/fstab, gjorde så att mappen monteras vid boot, genom att lägga till raden "10.0.0.4:/ /mnt/user_local nfs4 defaults 0 0"

## autofs och automount - [STO.7](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.7)
  ### 1. Vad är en automount map?
    Automount mapp är en konfigurationsfil som visar vart ett filsystem ska monteras
    
  ### 2. Vilket paket behöver du installera för att använda automount?
    autofs och autofs-ldap
  
  ### 3. Vad är det för skillnad på direkta och indirekta automount maps?
    I direkta automount mappar så definerar man specifika kataloger som ska monteras medans indirekta specifieras endast den översta katalogen och autofs hanterar katalogerna under.
  
  ### 4. Vad heter huvudkonfigurationsfilen för automount? Hur pekar den ut master-katalogen/map:en? Visa detta. Notera att detta inte är samma sak som auto.master.
    /etc/autofs.conf är huvudkonfigurationsfilen, det finns en rad i filen, "master_map_name = /etc/auto.master" som bestämmer vart master map filen ligger, som i sig pekar ut master-katalogen.

## autofs utan LDAP - [STO.8](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.8)
    La till användara autofs{1..2} via användarskaparskriptet och flyttade deras /home mappar till /home-storage{1..2}

    gjorde chown -R autofs1:autofs1 /home-storage1/autofs1 samt respektive för autofs2 för att ändra ägare.
    
    I /etc/exports, la till raderna:
      /home-storage1  10.0.0.2(rw,wdelay,root_squash,no_subtree_check,sec=sys,secure,no_all_squash)
      /home-storage1  10.0.0.3(rw,wdelay,root_squash,no_subtree_check,sec=sys,secure,no_all_squash)
      /home-storage2  10.0.0.2(rw,wdelay,root_squash,no_subtree_check,sec=sys,secure,no_all_squash)
      /home-storage2  10.0.0.3(rw,wdelay,root_squash,no_subtree_check,sec=sys,secure,no_all_squash)
    Exporterade alla med exportfs -a

  ### På klienterna
    Installerade autofs
    Gjorde /home till den indirekta monteringspunkten genom att lägga till raden: "/home /etc/auto.home" i /etc/auto.master
    I /etc/auto.home definerade vi varje användares subkatalog och vart den ska monteras genom att lägga till raderna:
      autofs1 -fstype=nfs4,rw,hard,intr 10.0.0.4:/home-storage1/autofs1
      autofs2 -fstype=nfs4,rw,hard,intr 10.0.0.4:/home-storage2/autofs2
    Nu när användaren loggar in så kommer användares huvudkatalog automatiskt monteras på nfs-servern.

    autofs1@client-1:~$ rm merv.txt 
    autofs1@client-1:~$ touch merv.txt
    autofs1@client-1:~$ nano merv.txt
    autofs1@client-1:~$ cat merv.txt 
    Bagagwa
    autofs1@client-1:~$ 
    
    autofs1@client-1:~$ cd ..
    autofs1@client-1:/home$ cd autofs2
    autofs1@client-1:/home/autofs2$ ls
    autofs1@client-1:/home/autofs2$ touch merv.txt
    touch: cannot touch 'merv.txt': Permission denied
    autofs1@client-1:/home/autofs2$ 


    

## autofs med LDAP - [STO.9](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.9)

  Paketen var redan installerade.
    
  Skapade autofs-ldap.ldif med innehåll:
  
      dn: cn=autofs,cn=schema,cn=config
      objectClass: olcSchemaConfig
      cn: autofs
      olcAttributeTypes: ( 1.3.6.1.4.1.2312.4.1.2 NAME 'automountInformation'
              DESC 'Information used by the autofs automounter'
              EQUALITY caseExactIA5Match
              SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 SINGLE-VALUE )
      olcObjectClasses: ( 1.3.6.1.4.1.2312.4.2.3 NAME 'automount' SUP top STRUCTURAL
              DESC 'An entry in an automounter map'
              MUST ( cn $ automountInformation $ objectClass )
              MAY ( description ) )
      olcObjectClasses: ( 1.3.6.1.4.1.2312.4.2.2 NAME 'automountMap' SUP top STRUCTURAL
              DESC 'A group of related automount objects'
              MUST ( ou ) )

      ldapadd -Y EXTERNAL -H ldapi:/// -f autofs-ldap.ldif
      SASL/EXTERNAL authentication started
      SASL username: gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth
      SASL SSF: 0
      adding new entry "cn=autofs,cn=schema,cn=config"

  Skapade en fil ou_ldap.ldif med innehåll:
  
        dn: ou=automount,dc=zorbak,dc=com
        objectClass: organizationalUnit
        ou: automount
        
        dn: ou=auto.home,ou=automount,dc=zorbak,dc=com
        objectClass: organizationalUnit
        ou: auto.home
  och använde ldapadd för att lägga till den.

  gjorde en annan ldif fil med detta innehåll:
  
        dn: cn=autofs1,ou=auto.home,ou=automount,dc=zorbak,dc=com
        objectClass: top
        objectClass: automount
        cn: autofs1
        automountInformation: /home-storage1/autofs1
        
        dn: cn=autofs2,ou=auto.home,ou=automount,dc=zorbak,dc=com
        objectClass: top
        objectClass: automount
        cn: autofs2
        automountInformation: /home-storage2/autofs2

  /etc/default/autofs på klient:
  
        #
        # Init system options
        #
        # If the kernel supports using the autofs miscellanous device
        # and you wish to use it you must set this configuration option
        # to "yes" otherwise it will not be used.
        #
        USE_MISC_DEVICE="yes"
        #
        # Use OPTIONS to add automount(8) command line options that
        # will be used when the daemon is started.
        #
        #OPTIONS=""
        #
        MASTER_MAP_NAME="ou=auto.master,ou=automount,dc=zorbak,dc=com"
        LDAP_URI="ldap://10.0.0.4"
        SEARCH_BASE="ou=automount,dc=zorbak,dc=com"
        
        MAP_OBJECT_CLASS="automountMap"
        ENTRY_OBJECT_CLASS="automount"
        MAP_ATTRIBUTE="ou"
        ENTRY_ATTRIBUTE="cn"
        VALUE_ATTRIBUTE="automountInformation"


  ### Autofs användarskript
    #!/usr/bin/python3.9
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"
    uid = 1000
    password = "password"
        
    def getPass():
        password = ""
        for i in range(1, 10):
            password += str(random.randint(0,9))
        return password
        
    def ldap(name, password):
        uid = subprocess.run(['id', '-u', name], capture_output=True, text=True, check=True).stdout.strip()
        subprocess.run(["ldapadduser", name, name, uid])
        subprocess.run(["ldapsetpasswd", name, password])
        path = ["/home-storage1/", "/home-storage2/"]
        path = path[random.randint(0, 1)]

        subprocess.run(["mkdir", path+name])
        subprocess.run(["chown", "-R", uid +":"+ uid, path+name])

        ldifContent = (f"dn: cn={name},ou=auto.home,ou=automount,dc=zorbak,dc=com\nobjectClass: automount\ncn: {name}\nautomountInformation: -fstype=nfs4,rw,hard,intr 10.0.0.4:{path}{name}\n")
        print(ldifContent)
        ldifName = f"tmp_{name}.ldif"
        file = open(ldifName, "w", encoding="utf-8")
        file.write(ldifContent)
        file.close()
        
        subprocess.run(["ldapadd", "-x", "-D", "cn=admin,dc=zorbak,dc=com", "-w", "password", "-H", "ldap:///", "-f", ldifName])
        
        
        
    with open(sys.argv[1], "rt", encoding="utf-8") as namefile:
        names = namefile.read()
        names = names.split("\n")
        for name in names:
            finalName = ""
            name = name.split()
            if name != "":
                name = (name[0][:3] + name[-1][:2]).lower()
                for letter in name:
                    good = False
                    for x in range(len(alphabet)):
                        if x <= 9:
                            if letter == numbers[x]:
                                good = True
                        if letter == alphabet[x]:
                            good = True
                        
                    if good:
                        finalName += letter
                    else:
                        finalName += alphabet[random.randint(0,(len(alphabet)-1))]

                finalName = (finalName + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
                password = getPass()
                subprocess.run(['useradd', '-ms', '/bin/bash', finalName ])
                subprocess.run(['passwd', finalName], input=f"{password}\n{password}\n", text=True)
                
                ldap(finalName, password)
                #print("ID: " + finalName)
                #print("Password: " + password)
            else:
                print("Account creation complete")

    







## Testning av NFS-servern och autofs - [STO.10](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.10)















