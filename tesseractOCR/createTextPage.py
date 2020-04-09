import os
import sys


for root, dirs, files in os.walk("/var/www/html/input"):
	for file in files:
		if file.endswith(".tif"):
			print (file)
			file_name = os.path.splitext(file)[0]

			print (file_name)

			cmd = 'tesseract '+ file + ' /var/www/html/input/data/'+ file_name +' -l tam'

			os.system(cmd)


	break
