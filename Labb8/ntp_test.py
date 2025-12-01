import subprocess

HOSTNAME = open("/etc/hostname", "r").read().strip()

def test_config():
	result = subprocess.run("cat /etc/ntp.conf | grep iburst", shell=True, stdout=subprocess.PIPE)
	result = result.stdout.decode("utf-8").split()
	print(result[1])

	if HOSTNAME != "gw":
		assert result[1] == "10.0.0.1"
	else:
		assert result[1] == "se.pool.ntp.org"

def test_queries():
	result = subprocess.run("ntpq -p | grep '*' ", shell=True, stdout=subprocess.PIPE)
	result = result.stdout.decode("utf-8").split()

	print(result[0])
	if HOSTNAME != "gw":
		assert result[0] == "*gw.zorbak.com"
	else:
		assert result[0][0] == "*"


	print(result[-2])
	assert float(result[-2]) < 1.5 and float(result[-2]) > -1.5

test_queries()
test_config()
