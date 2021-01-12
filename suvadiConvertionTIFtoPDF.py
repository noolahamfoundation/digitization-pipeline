import img2pdf
import os
import subprocess
from PyPDF2 import PdfFileReader, PdfFileWriter

# This Script can be used to convert TIF files to PDF by looping through every folders
# The modules used here are:
# img2pdf pip3 install img2pdf
# GhostScript

rootdir = '/media/noolaham/Transcend/EAP1260/EAP1260_C034'
pdf = '/home/noolaham/Pictures/pdf'
singlePagePDF = '/home/noolaham/Pictures/singlePdf'
outputfolder = '/home/noolaham/Pictures/finalpdf'

for subdir, dirs, files in os.walk(rootdir):
	pdfname = ""

	if not os.path.exists(pdf):
		os.mkdir(pdf)

	if not os.path.exists(singlePagePDF):
		os.mkdir(singlePagePDF)

	for file in sorted(files):

		if file.endswith(".tif") or file.endswith(".TIF"):

			filename = str(file).replace('.TIF','')
			gmp = 'img2pdf --output '+pdf+'/'+filename+'.pdf '+subdir+'/'+file
			
			subprocess.call(gmp, shell=True)

			infile = PdfFileReader(pdf+'/'+filename+'.pdf', 'rb')
			output = PdfFileWriter()
			p = infile.getPage(0)
			output.addPage(p)
			with open(singlePagePDF+'/'+filename+'.pdf', 'wb') as f:
				output.write(f)

		pdfname = os.path.basename(subdir)

	for subdir, dirs, files in os.walk(singlePagePDF):
		filesName = []

		for pdfFile in sorted(files):
			filesName.append(singlePagePDF+'/'+pdfFile)
	
		str1 = ' '.join(filesName)

		cmd = 'gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE='+pdfname+'.pdf -dBATCH '+ str1
		subprocess.call(cmd, shell=True)

	gmp1 = 'rm -r '+pdf
	subprocess.call(gmp1, shell=True)

	gmp2 = 'rm -r '+singlePagePDF
	subprocess.call(gmp2, shell=True)
