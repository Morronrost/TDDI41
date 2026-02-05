## Shebang - [SCT.1](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sct/index.sv.shtml#sct.1)
    1. Vad är en shebang? Och hur används det?
      En shebang är skrivs längst upp i din skriptkod och berättar vägen till kompilatorn som kommer att skriva om koden till maskinkod.
      t.ex "#!/usr/bin/python3.9"
      
## Skript för att automatiskt skapa användarkonto - [SCT.2](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sct/index.sv.shtml#sct.2)
        #!/usr/bin/python3.9

        import random, sys, string, os, subprocess
        
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        numbers = "0123456789"
        password = "password"
        
        def getPass():
        	password = ""
        	for i in range(1, 10):
        		password += str(random.randint(0,9))
        	return password
        
        with open(sys.argv[1], "rt", encoding="utf-8") as namefile:
            names = namefile.read()
            names = names.split("\n")
            for name in names:
                finalName = ""
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
                
                #print("ID: " + finalName)
                #print("Password: " + password)

    

## Skript för automatiserad testning - [SCT.3](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sct/index.sv.shtml#sct.3)
    #!/usr/bin/python3.9
    
    import subprocess
    
    def test_root():
    	user = "root"
    	test = subprocess.run('cat /etc/passwd | grep ' + user, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
    
    	assert test.returncode == 0
    
    def test_noshell():
    	user = "games"
    	file = open("/etc/shells", "rt")
    	shellList = file.read().split("\n")
    	for shells in shellList[1:(len(shellList)-1)]:
    		test = subprocess.run('cat /etc/passwd | grep ' + user + '| grep ' + shells , stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell = True)
    		assert test.returncode == 1
    
    test_root()
    test_noshell()
    


