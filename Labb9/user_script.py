#!/usr/bin/python3.9

import random, sys, string, os, subprocess
    
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
