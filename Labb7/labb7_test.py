import subprocess

HOSTNAME = open("/etc/hostname", "r").read().strip()

def test_services():
	nslcdResult = subprocess.run("service nslcd status | grep active", shell=True, stdout=subprocess.PIPE)
	nslcdResultDecoded = nslcdResult.stdout.decode("utf-8").split()[1]
	assert nslcdResultDecoded == "active"


	slapdResult = subprocess.run("service slapd status | grep active", shell=True, stdout=subprocess.PIPE)
	slapdResultDecoded = slapdResult.stdout.decode("utf-8").split()[1]
	assert slapdResultDecoded == "active"


def print_nsswitch():
	result = subprocess.run("cat /etc/nsswitch.conf | grep ldap", shell=True, stdout=subprocess.PIPE)
	resultDecoded = result.stdout.decode("utf-8").split()
	assert resultDecoded[0] == "passwd:"
	assert resultDecoded[3] == "group:"
	assert resultDecoded[6] == "shadow:"

	result = subprocess.run("getent passwd | grep c1", shell=True, stdout=subprocess.PIPE)
	resultDecoded = result.stdout.decode("utf-8").split(":")[0]

	assert resultDecoded == "c1"

def test_ldapsearch():
	result = subprocess.run("ldapsearch -x | grep zorbak.com", shell=True, stdout=subprocess.PIPE)
	resultDecoded = result.stdout.decode("utf-8").split()
	assert resultDecoded[1] == "zorbak.com"

if HOSTNAME == "server":
	test_services()
print_nsswitch()
test_ldapsearch()
