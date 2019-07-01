# Optimize PDF files and make a batch folder and create subfolders for every optimized files

import os
import sys
import glob
from shutil import move

# Change the uncompressed_pdf path to proper file path where unoptimized PDF exists
uncompressed_pdf = "/home/noolaham/Desktop/unoptimizedPDF"

# Configure the batch_folder path to save the optimized PDF files finally
batch_folder = "/home/noolaham/Documents"

for root, dirs, files in os.walk(uncompressed_pdf):
	for file in files:
		if file.endswith(".pdf"):
			print (file)
			cmdCompress = 'gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dColorImageResolution=150 -sOutputFile='+batch_folder+ '/'+ file + ' ' + file

			os.system(cmdCompress)
	
	break

def calculate_folder_num(noolaham_id):
    noolaham_id = int(noolaham_id)
    folder_id = (noolaham_id//100) + 1
    folder_id = str(folder_id).zfill(2)
    return folder_id

pdf_file_name = os.listdir(batch_folder)[0]
noolaham_id = os.path.splitext(pdf_file_name)[0]
folder_id = calculate_folder_num(noolaham_id)

# Create batch_folder
if not os.path.exists(batch_folder + "/" + folder_id):
    os.makedirs(batch_folder + "/" + folder_id)

pdf_count = 0
for pdf_path in glob.glob(batch_folder + "/*.pdf"):
    noolaham_id = os.path.splitext(os.path.basename(pdf_path))[0]
    print("processing " + noolaham_id)
    pdf_in_folder_path = batch_folder + "/" + folder_id + "/" + noolaham_id + "/" + noolaham_id + ".pdf"
    
    # Create folder
    if not os.path.exists(batch_folder + "/" + folder_id + "/" + noolaham_id):
        os.makedirs(batch_folder + "/" + folder_id + "/" + noolaham_id)
        
	## move pdf
    move(pdf_path, pdf_in_folder_path)
    pdf_count = pdf_count + 1
    
print("Total files processed: " + str(pdf_count))

