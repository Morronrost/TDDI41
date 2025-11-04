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
