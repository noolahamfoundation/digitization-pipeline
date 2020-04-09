# -*- coding: utf-8 -*-
import urllib
import ftplib
import os
import csv
import sys
from string import Template
from wikitools import wiki
from wikitools import api

def getNoolahamToken(i_site, i_api):
     params = {'action':'query', 'prop':'info','intoken':'edit','titles':'1'}
     req = i_api.APIRequest(i_site, params)
     response = req.query(False)
     token = response['query']['pages']['-1']['edittoken']
     return token

def updateWikiPage(i_site, i_api, i_token, i_titlePage, i_updateText):
     params = {'action':'edit', 'title':i_titlePage, 'token':i_token,  'text': i_updateText}
     request = i_api.APIRequest(i_site, params)
     result = request.query()
     print result
     return

def getCatsText(i_catsStr):
    catsList = i_catsStr.split(";")
    catText = "\n"
    for cat in catsList:
	if cat != "-":
        	catText = catText = "[[பகுப்பு:" + cat + "]]\n"
    return catText

def prepareWikiPage(i_row):
    pgNumber = i_row[0]
    pgFolderPath = i_row[1]
    pgTitle = i_row[2].strip()
    pgDate = i_row[3].strip()
    pgYear = pgDate[:4]
    pgMonth = pgDate[5:7]
    pgDay = pgDate[8:]
    pgContentType = i_row[4].strip()
    pgLanguage = i_row[6]
    pgPeriodicity = i_row[7].strip()
    pgPermission = i_row[12]
    pgPages = i_row[13]
    pgAuthor = i_row[8]
    pgPublisher = i_row[9]
    pgCats = i_row[16]
    pgCategory = i_row[17]


    pdfUrl = "http://noolaham.net" + pgFolderPath + "/" + pgNumber + ".pdf"
    pdfLink = "\n<!--pdf_link-->* [" + pdfUrl + " " + pgTitle + "] {{P}}<!--pdf_link-->\n"

    pageParamsDict = {'contentType':pgContentType, 'title':pgTitle, 'number':pgNumber, 'date':pgDate, 'year':pgYear, 'pages':pgPages, 'langauge':pgLanguage, 'periodicity': pgPeriodicity, 'permission':  pgPermission, 'month':pgMonth, 'day':pgDay, 'author':pgAuthor, 'publisher':pgPublisher, 'cats':pgCats, 'category':pgCategory}

    pageText = ""
    if pgContentType == "இதழ்":
        pageText = """{{$contentType|
    நூலக எண் = $number |
    வெளியீடு = [[:பகுப்பு:$year|$year]].$month.$day  |
    சுழற்சி = $periodicity |
    இதழாசிரியர் = [[:பகுப்பு:$author|$author]] |
    மொழி = $langauge |
    பதிப்பகம் = [[:பகுப்பு:$publisher|$publisher]] |
    பக்கங்கள் = $pages |
    }}

=={{Multi|வாசிக்க|To Read}}==
"""

    if pgContentType == "சிறப்புமலர்" or pgContentType == "நூல்" or pgContentType == "நினைவுமலர்":

        pageText = """{{$contentType|
    நூலக எண் = $number |
    வெளியீடு = [[:பகுப்பு:$year|$year]].$month.$day  |
    ஆசிரியர் = [[:பகுப்பு:$author|$author]] |
    வகை = $category|
    மொழி = $langauge |
    பதிப்பகம் = [[:பகுப்பு:$publisher|$publisher]] |
    பதிப்பு = [[:பகுப்பு:$year|$year]] |
    பக்கங்கள் = $pages |
    }}

=={{Multi|வாசிக்க|To Read}}==
"""

    if pgContentType == "பத்திரிகை":

        tamilMonths = {"01":"தை", "02":"மாசி", "03":"பங்குனி", "04":"சித்திரை", "05":"வைகாசி", "06":"ஆனி", "07":"ஆடி", "08":"ஆவணி", "09":"புரட்டாதி", "10":"ஐப்பசி", "11":"கார்த்திகை", "12":"மார்கழி"}
        #pgMonth = translate(pgMonth, tamilMonths)
        pageParamsDict["month"] = pgMonth

        pageText = """{{பத்திரிகை|
    நூலக எண் = $number |
    வெளியீடு = [[:பகுப்பு:$year|$year]].$month.$day |
    சுழற்சி = $periodicity |
    இதழாசிரியர் = [[:பகுப்பு:$author|$author]] |
    பதிப்பகம் = $publisher |
    மொழி = $langauge |
    பக்கங்கள் = $pages |
    }}

=={{Multi|வாசிக்க|To Read}}==
"""

    paramReplace = Template(pageText)
    pageText = paramReplace.substitute(pageParamsDict)

    if pgPermission == "வெளியிடப்படாது":
	pdfLink = "\n{{வெளியிடப்படாது}}"

    if pgPermission == "வெளியிடப்படும்":
	pdfLink = "\n{{வெளியிடப்படும்}}"  

    if pgPermission == "தமிழ் Mirror":
	pdfLink = "\n{{தமிழ் Mirror}}"  

    #Add pdf link
    pageText = pageText +  pdfLink;

    #Add year category
    if pgYear != "-":
	pageText = pageText + "\n\n" + "[[பகுப்பு:" + pgYear + "]]";
    if pgAuthor != "-":
	pageText = pageText + "\n\n" + "[[பகுப்பு:" + pgAuthor + "]]"; 

    if pgContentType != "பத்திரிகை" or pgContentType != "இதழ்":
    	pageText = pageText + "\n\n" + "[[பகுப்பு:" + pgPublisher + "]]";

    #Add other categories
    catsStr = getCatsText(pgCats)
    pageText = pageText + catsStr

    return pageText


def translate(string, wdict):
    for key in wdict:
        string = string.replace(key, wdict[key].lower())
    return string.upper()

# create a Wiki object
site = wiki.Wiki("http://www.noolaham.org/wiki/api.php")

# login - required for read-restricted wikis
if not site.login("username","password", verify=True):
    print("Login failed")

#Get Token (needed to edit wiki)
token = getNoolahamToken(site, api)

#Read through each entry and update wiki
batchfile = open('createdata.csv', 'rt')
try:
     reader = csv.reader(batchfile)
     for row in reader:
	pgTitle = row[2]
        pageText = prepareWikiPage(row)
	with open("test.txt", "w") as e:
		e.write(pageText)
        print(pageText)

       	#updateWikiPage(site, api, token, pgTitle, pageText)

finally:
     batchfile.close()
