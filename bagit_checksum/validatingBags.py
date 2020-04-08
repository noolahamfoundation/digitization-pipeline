'''

The script should be run on Python 3.
Run the script by providing the root directory path.

This will extract the zip folders and compare the manifest and give the result.

'''

import os
import sys
import bagit
import tempfile
import subprocess
import zipfile

rootdir = '/home/user/Documents/checksum1'

#--------- Do not change below unless you are in doubt ----

def validate_bag(path_to_bag):

	print(path_to_bag)

	with tempfile.TemporaryDirectory() as tmpdirname:
		print('Created temporary directory:', tmpdirname)

		zip_ref = zipfile.ZipFile(path_to_bag, 'r')
		zip_ref.extractall(tmpdirname)

		bag_basename = os.path.basename(path_to_bag)
		folder_name = os.path.splitext(bag_basename)[0]

		print(folder_name)
		bag_extracted_path = tmpdirname + "/" + folder_name 
		bag = bagit.Bag(bag_extracted_path)

		if bag.is_valid():
			return True
		else:
			return False

for subdir, dirs, files in os.walk(rootdir):
	for file in files:

		print("Processing " + file)
		validation_status = False
		try:
			validation_status = validate_bag(subdir+'/'+file)
		except:
			print("Unexpected error:", sys.exc_info()[0])

		print("Validation Status for " + file + " : " + str(validation_status))
