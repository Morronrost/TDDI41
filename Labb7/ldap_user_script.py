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


with open(sys.argv[1], "rt", encoding="utf-8") as namefile:
    names = namefile.read()
    names = names.split("\n")
    for name in names:
            finalName = ""
            if name != "":
                name = name.split()
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