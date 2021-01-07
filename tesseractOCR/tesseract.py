import os

dir_name = "/var/www/html/text/"

with open("71647.html", "w") as e:
	e.write("<!DOCTYPE html>\n<html>\n<head>\n<meta charset='UTF-8'>")
	e.write("\n<style>")
	e.write("\n#notice, pre {")
	e.write("\nwidth: 620px;")
	e.write("\nwhite-space: pre-wrap;")
	e.write("\nwhite-space: -moz-pre-wrap;")
	e.write("\nwhite-space: -pre-wrap;")
	e.write("\nwhite-space: -o-pre-wrap;")
	e.write("\nword-wrap: break-word;")
	e.write("\n}\n</style>")
	e.write("\n<title>விடியல்: யா/ சாவகச்சேரி இந்துக் கல்லூரி 2014\n</title>")
	e.write("\n</head>\n<body>")
	e.write("\n<div id='notice'>")
	e.write("\n<font face='Latha' size='2'><font color='#FF0000'>கவனிக்க: </font>")
	e.write("இந்த மின்னூலைத் தனிப்பட்ட வாசிப்பு, உசாத்துணைத் தேவைகளுக்கு மட்டுமே பயன்படுத்தலாம். வேறு பயன்பாடுகளுக்கு ஆசிரியரின்/பதிப்புரிமையாளரின் அனுமதி பெறப்பட வேண்டும்.")
	e.write("\n<br>இது கூகிள் எழுத்துணரியால் தானியக்கமாக உருவாக்கப்பட்ட கோப்பு. இந்த மின்னூல் மெய்ப்புப் பார்க்கப்படவில்லை.")
	e.write("\n<br>இந்தப் படைப்பின் நூலகப் பக்கத்தினை பார்வையிட பின்வரும் இணைப்புக்குச் செல்லவும்:  ")
	e.write("<b><a href='http://noolaham.org/wiki/index.php/") 
	e.write("' target='_blank'>விடியல்: யா/ சாவகச்சேரி இந்துக் கல்லூரி 2014'</a></b>")
	e.write("\n</font>\n</div>\n<hr>")

	for i in range(1,13):
		condents = dir_name +'/'+ str(i)+'.txt'
		text_files = open(str(i)+'.txt',"r")
		e.write("\n<pre>")
		e.write("\nPage " + str(i))
		for lines in text_files.readlines():
			e.write(lines)
		e.write("\n</pre>")
		e.write("\n<hr/>")

	e.write("</body></html>")

