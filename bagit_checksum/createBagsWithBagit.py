'''

The script should be run on Python 3.
Run the script by providing the root directory path.
This will create the bagit bags for every Books folder

'''

import os
import bagit

rootdir = '/media/noolaham/Transcend/73001-74000'

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if ".pdf" in file:
			print("Creating bag for: ", subdir)
			bag = bagit.make_bag(subdir, {'Contact-Name': 'Noolaham Foundation'})
		else:
			continue;
