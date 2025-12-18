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
    Skapade en mapp /mnt/user_local och sedan monterade /usr/local från servern till den.
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
      autofs1 -fstype=nfs4, rw, nosuid, soft nfs-10.0.0.4:/home-storage1/autofs1
      autofs2 -fstype=nfs4, rw, nosuid, soft nfs-10.0.0.4:/home-storage2/autofs2
    Nu när användaren loggar in så kommer användares huvudkatalog automatiskt monteras på nfs-servern.

## autofs med LDAP - [STO.9](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.9)

## Testning av NFS-servern och autofs - [STO.10](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.10)











