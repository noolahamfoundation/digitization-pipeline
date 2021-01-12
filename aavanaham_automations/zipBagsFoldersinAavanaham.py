import os
import subprocess

rootdir = "/home/bags"

for subdir, dirs, files in os.walk(rootdir):

	for folders in dirs:

		cmd = "sudo zip -r "+ folders+".zip " +folders
		subprocess.call(cmd, shell=True)

		subprocess.call(['sudo','rm', '-rf', folders])
