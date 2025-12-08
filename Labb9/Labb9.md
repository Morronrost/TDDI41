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
    

## Konfigurering av NFS - [STO.6](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.6)

## autofs och automount - [STO.7](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.7)
  ### 1. Vad är en automount map?
  
  ### 2. Vilket paket behöver du installera för att använda automount?
  
  ### 3. Vad är det för skillnad på direkta och indirekta automount maps?
  
  ### 4. Vad heter huvudkonfigurationsfilen för automount? Hur pekar den ut master-katalogen/map:en? Visa detta. Notera att detta inte är samma sak som auto.master.

## autofs utan LDAP - [STO.8](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.8)

## autofs med LDAP - [STO.9](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.9)

## Testning av NFS-servern och autofs - [STO.10](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sto/index.sv.shtml#sto.10)






