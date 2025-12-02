## Grunderna i LDAP - [LDAP.1](https://www.ida.liu.se/~TDDI41/2025/uppgifter/ldap/index.sv.shtml#ldap.1)
  ### 1.Vad betyder DIT och hur fungerar det?
       DIT står för Directory Information Tree. Alltså är det ett hierarkiskt träd som innehåller entries i LDAP.
       Varje entry har ett unikt "Distinguished Name" samt flera attributes som i sig innehåller en key samt en eller flera värden. Varje attribut är definierad i minst en objectClass.
       Attribut och objectClass är sig definierade i ett schema då objectClass räknas som ett speciellt attribut.
       
  ### 2. Vad betyder förkortningarna dn och dc och hur används de?
        DN står för Distinguished Name och är en unik identifierare till en entry i katalogen. DC står för Domain Component och är en del av dn
        som reprensenterar en komponent av domännamnet. T.ex example i example.com
        
  ### 3. Vad är ett attribute?
        Ett attribute innehåller en key samt en eller flera värden. Varje värde måste vara definierad i minst en objectClass.
       
  ### 4. Vad är en "object class"?
        Object class är ett speciellt attribut som defineras inom ett schema. Object class kan vara en attribute container eller en sökoperation.
        En object class har ett namn eller identifierare som är unikt globalt.
        
  ### 5. Vad är det för skillnad mellan en "structural-" och en "auxiliary object class?
        En strukturell objektklass är den primära klassen och kan inte ändras. Auxilliära objektklasser kan vara flera och ändras eller tas bort.
        Varje objekt måste ha en strukturell objektklass men behöver inte ha någon auxilliär.

## Konfigurering av LDAP - [LDAP.2](https://www.ida.liu.se/~TDDI41/2025/uppgifter/ldap/index.sv.shtml#ldap.2)
  ### Ldapsearch
        root@gw:~# ldapsearch -x
        # extended LDIF
        #
        # LDAPv3
        # base <dc=zorbak,dc=com> (default) with scope subtree
        # filter: (objectclass=*)
        # requesting: ALL
        #

        # zorbak.com
        dn: dc=zorbak,dc=com
        objectClass: top
        objectClass: dcObject
        objectClass: organization
        o: zorbak
        dc: zorbak

        # users, zorbak.com
        dn: ou=users,dc=zorbak,dc=com
        ou: users
        objectClass: organizationalUnit

        # c1, users, zorbak.com
        dn: uid=c1,ou=users,dc=zorbak,dc=com
        objectClass: posixAccount
        objectClass: inetOrgPerson
        cn: client-1
        sn: client
        uidNumber: 101
        gidNumber: 101
        homeDirectory: /etc/ldap/c1
        uid: c1

        # search result
        search: 2
        result: 0 Success

        # numResponses: 5
        # numEntries: 4
        
  ### Check if nslcd service is running
        root@gw:~# systemctl list-units --type=service --state=running | grep nslcd
        nslcd.service            loaded active running LSB: LDAP connection daemon

## Lägga till en användare i LDAP med LDIF-fil - [LDAP.3](https://www.ida.liu.se/~TDDI41/2025/uppgifter/ldap/index.sv.shtml#ldap.3)
  ### Ldif-fil för organizational unit
    dn: ou=users, dc=zorbak,dc=com
    ou: users
    objectClass: organizationalUnit
    
  ### Ldif-fil för user
    dn: uid=c1, ou=users, dc=zorbak,dc=com
    objectClass: posixAccount
    objectClass: inetOrgPerson
    cn: client-1
    sn: client
    uidNumber: 101
    gidNumber: 101
    homeDirectory: /etc/ldap/c1
    userPassword: password

  ### Lägg till organizational unit
      root@server:~# ldapadd -x -D "cn=admin,dc=zorbak,dc=com" -W -f User.ldif
      adding new entry "ou=users,dc=zorbak,dc=com"
    
  ### Lägg till user
      root@server:~# ldapadd -x -D "cn=admin,dc=zorbak,dc=com" -W -f User.ldif
      adding new entry "uid=c1,ou=users,dc=zorbak,dc=com"

  ### Ldapsearch
        root@gw:~# ldapsearch -x
        # extended LDIF
        #
        # LDAPv3
        # base <dc=zorbak,dc=com> (default) with scope subtree
        # filter: (objectclass=*)
        # requesting: ALL
        #

        # zorbak.com
        dn: dc=zorbak,dc=com
        objectClass: top
        objectClass: dcObject
        objectClass: organization
        o: zorbak
        dc: zorbak

        # users, zorbak.com
        dn: ou=users,dc=zorbak,dc=com
        ou: users
        objectClass: organizationalUnit

        # c1, users, zorbak.com
        dn: uid=c1,ou=users,dc=zorbak,dc=com
        objectClass: posixAccount
        objectClass: inetOrgPerson
        cn: client-1
        sn: client
        uidNumber: 101
        gidNumber: 101
        homeDirectory: /etc/ldap/c1
        uid: c1

        # search result
        search: 2
        result: 0 Success

        # numResponses: 5
        # numEntries: 4
  ### getent
      root@client-2:~# getent passwd | grep c1
      c1:*:101:101:client-1:/etc/ldap/c1
  
  ### login
      root@server:/etc/ldap# ssh c1@zorbak.com
      c1@zorbak.com's password: 
      Linux server 5.10.0-15-amd64 #1 SMP Debian 5.10.120-1 (2022-06-09) x86_64
      
      The programs included with the Debian GNU/Linux system are free software;
      the exact distribution terms for each program are described in the
      individual files in /usr/share/doc/*/copyright.
      
      Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
      permitted by applicable law.
      Last login: Tue Dec  2 14:42:57 2025 from 10.0.0.4
      $ 


## Lägga till en användare i LDAP med ldapscripts - [LDAP.4](https://www.ida.liu.se/~TDDI41/2025/uppgifter/ldap/index.sv.shtml#ldap.4)
        root@server:~# echo -n 'password' | tee /etc/ldapscripts/ldapscripts.passwd password
        
  ### Ldapscripts.conf
        # LDAP server
        # DEBIAN: value from /etc/nslcd.conf (uri) is used.
        SERVER="ldap://10.0.0.4"
        
        # Suffixes
        # DEBIAN: values from /etc/nslcd.conf (base maps) are used.
        SUFFIX="dc=zorbak,dc=com" # Global suffix
        GSUFFIX="ou=groups"        # Groups ou (just under $SUFFIX)
        USUFFIX="ou=users"         # Users ou (just under $SUFFIX)
        MSUFFIX="ou=machines"      # Machines ou (just under $SUFFIX)
        
        # Simple authentication parameters
        # The following BIND* parameters are ignored if SASLAUTH is set
        BINDDN="cn=admin,dc=zorbak,dc=com"
        # The following file contains the raw password of the BINDDN
        # Create it with something like : echo -n 'secret' > $BINDPWDFILE
        # WARNING !!!! Be careful not to make this file world-readable
        BINDPWDFILE="/etc/ldapscripts/ldapscripts.passwd"
        # For older versions of OpenLDAP, it is still possible to use
        # unsecure command-line passwords by defining the following option
        # AND commenting the previous one (BINDPWDFILE takes precedence)
        #BINDPWD="secret"
        
        # Start with these IDs *if no entry found in LDAP*
        GIDSTART="100" # Group ID
        UIDSTART="100" # User ID
        MIDSTART="20000" # Machine ID

  ### Lägga till användare
        root@server:~# ldapadduser c2 101
        Successfully added user c2 to LDAP
        Successfully set password for user c2
        root@server:~# ldapsetpasswd c2 password
        Successfully set encoded password for user uid=c2,ou=users,dc=zorbak,dc=com

  ### login
        root@server:/etc/ldapscripts# ssh c2@zorbak.com
        c2@zorbak.com's password: 
        Linux server 5.10.0-15-amd64 #1 SMP Debian 5.10.120-1 (2022-06-09) x86_64
        
        The programs included with the Debian GNU/Linux system are free software;
        the exact distribution terms for each program are described in the
        individual files in /usr/share/doc/*/copyright.
        
        Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
        permitted by applicable law.
        Last login: Tue Dec  2 14:52:36 2025 from 10.0.0.4
        $ 

## Lägga till flera användare i LDAP med ldapscripts - [LDAP.5](https://www.ida.liu.se/~TDDI41/2025/uppgifter/ldap/index.sv.shtml#ldap.5)

## Testning av LDAP-konfiguration och verktyg - [LDAP.6](https://www.ida.liu.se/~TDDI41/2025/uppgifter/ldap/index.sv.shtml#ldap.6)

