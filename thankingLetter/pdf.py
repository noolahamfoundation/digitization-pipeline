import zipfile
import docx
import PyPDF2  

replaceText = {"{donarName}" : "கணேசன்", "{letterDate}" : "May 31, 2013", "{amount}" : "23000", "{depositDate}" : "08.02.2021"}
templateDocx = zipfile.ZipFile("/var/www/html/letter2/original.docx")
newDocx = zipfile.ZipFile("/var/www/html/letter2/new.docx", "a")


with open(templateDocx.extract("word/document.xml", "C:/")) as tempXmlFile:
    tempXmlStr = tempXmlFile.read()

for key in replaceText.keys():
    tempXmlStr = tempXmlStr.replace(str(key), str(replaceText.get(key)))

with open("C:/temp.xml", "w+") as tempXmlFile:
    tempXmlFile.write(tempXmlStr)

for file in templateDocx.filelist:
    if not file.filename == "word/document.xml":
        newDocx.writestr(file.filename, templateDocx.read(file))

newDocx.write("C:/temp.xml", "word/document.xml")

templateDocx.close()
newDocx.close()


