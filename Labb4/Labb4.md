## Shebang - [SCT.1](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sct/index.sv.shtml#sct.1)
    1. Vad är en shebang? Och hur används det?
      En shebang är skrivs längst upp i din skriptkod och berättar vägen till kompilatorn som kommer att skriva om koden till maskinkod.
      t.ex "#!/usr/bin/python3.9"
      
## Skript för att automatiskt skapa användarkonto - [SCT.2](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sct/index.sv.shtml#sct.2)
    #!/usr/bin/python3.9
    import random, sys, string, os, subprocess
  
    namelist = open("names-tricky", "rt")
    alf = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
    
    def getPass():
    	password = ""
    	for i in range(1, 10):
    		password += str(random.randint(0,9))
    	return password
    
    #with open(sys.argv[1], "rt") as namefile:
    
    	#for name in namefile.read():
    
    for name in namelist:
    	rand1 = random.randint(0,9)
    	rand2 = random.randint(0,9)
    	rand3 = random.randint(0,9)
    
    	for char in name:
    		if alf.find(char) == -1:
    			randChar = chr(random.randint(ord('a'), ord('z')))
    			name = name.replace(char, randChar)
    
    	liuid = name[:3] + str(rand1) + str(rand2) + str(rand3)
    	password = getPass()
    	#try:
    	subprocess.run(['useradd', '-ms', '/bin/bash', liuid ])
    	subprocess.run(['passwd', liuid], input=f"{password}\n{password}\n", text=True)
    	#except:
    	#	print(f"Failed to add user.")
    	#	sys.exit(1)
    	print("LiuId: " + liuid)
    	print("Password: " + password)

## Skript för automatiserad testning - [SCT.3](https://www.ida.liu.se/~TDDI41/2025/uppgifter/sct/index.sv.shtml#sct.3)
    #!/usr/bin/python3.9
    namelist = open("/courses/TDDI41/names-tricky", "rt")
    print(namelist)
