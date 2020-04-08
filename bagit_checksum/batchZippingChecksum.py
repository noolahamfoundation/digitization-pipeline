'''

The script should be run on Python 3.
Run the script by providing the root directory path.

This will zip the every books folder and after that it will delete the folder.

'''

import os
import subprocess

rootdir = '/media/noolaham/Transcend/73001-74000'

def zipAndDelete(rootdir):
    
    for subdir, dirs, files in os.walk(rootdir):
        for folders in dirs:
            if os.path.isdir(subdir+'/data'):
                folderName = os.path.dirname(subdir)
                os.chdir(folderName)
                
                folder_name = os.path.basename(subdir)
                
                print("Zipping the folder: ", subdir)
                
                cmd = 'zip -1 -r "'+subdir+ '".zip ' + folder_name
                subprocess.call(cmd, shell=True)

                print("Deleting: ", subdir)
                subprocess.call(['rm', '-rf', subdir])
            

zipAndDelete(rootdir)
