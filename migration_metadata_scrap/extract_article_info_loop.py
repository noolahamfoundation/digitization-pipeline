#!/usr/bin/env python
# coding: utf-8

# 2nd Script to extract the metadata from the articles
# This needs Python 2 for the wikitools library
# The wikitools library is not compatible with Python 3
# You can run this script in a Python 2 environment

import csv
import wikitools
import os
import sys
import pandas as pd

wiki_url = "https://noolaham.org/wiki/api.php"

df = pd.DataFrame()

missedDf = pd.DataFrame()

def clean_quotes(text):
    # Check if the string starts and ends with double quotes
    if text.startswith('"') and text.endswith('"'):
        # Remove the double quotes from the start and end
        text = text[1:-1]
    return text

for i in range (100, 119):

    batchfile = open('./first_list/books_and_authors_{}.csv'.format(i), 'rt')

    reader = csv.reader(batchfile)
    next(reader, None)

    for row in reader:
        book_title = clean_quotes(row[1].strip())
        pagename = str(book_title)
        
        try:
        
            wiki = wikitools.wiki.Wiki(wiki_url)

            page = wikitools.Page(wiki,  pagename , followRedir=True)
        
            template =  page.getWikiText().split("{{")[1].split("}}")[0]
        
            template1 =  page.getWikiText().split("|")[0]

            metaData = ['-'] * 16

            resource_type = template1.replace("{","")

            print(template)
        
            for i in template.split("\n"):    
                if "=" in i:
                    key = i.split("=")[0].strip()
                    value = i.split("=")[1].strip()
            
                    if key == "தலைப்பு":
                        value = value.replace("'","")
            
                    if value[-1] == "|" :
                        value = value[:-1]
                
                    if "[[:பகுப்பு" in value:
                        value3 = ""
                        value2 = value.split("|")[1].strip().replace("]", "")
                        value3 = value.split("[[:")[0].strip()
                        if value3 == "":
                            value = value2
                        else:
                            value = value3 + ' ' + value2

                    if key == "படிமம்":
                        continue
            
                    #1 resource type
                    metaData[0] = resource_type

                    #2 noolaham no.
                    if key == "நூலக எண்":
                        metaData[1] = value
            
                    #3 heading
                    metaData[2] = pagename

                    #4 author
                    if key == "ஆசிரியர்":
                        metaData[3] = value.decode('utf-8')
            
                    # 8 publisher    
                    if key == "பதிப்பகம்":
                        metaData[4] = value.decode('utf-8')

                    #9 Veliyeeddaandu
                    if key == "வெளியீட்டாண்டு":
                        metaData[5] = value.decode('utf-8')

                    #10 pathippu
                    if key == "பதிப்பு":
                        metaData[6] = value.decode('utf-8')

                    #11 moli
                    if key == "மொழி":
                        metaData[7] = value.decode('utf-8')
                    
                    #12 vagai
                    if key == "வகை":
                        metaData[8] = value.decode('utf-8')
                
                    #14 Pages
                    if key == "பக்கங்கள்":
                        metaData[10] = value.decode('utf-8')
                
                    if key == "இதழாசிரியர்":
                        metaData[13] = value.decode('utf-8')
                    if key == "வெளியீடு":
                        metaData[14] = value.decode('utf-8')
                    if key == "சுழற்சி":
                        metaData[15] = value.decode('utf-8')
        
            pageText = page.getWikiText().strip();
            
            print metaData[1]
        
            #13 category    
            categories = ""
        
            for i in pageText.split("\n"):        
                if "[[பகுப்பு:" in i:
                    value = i.split("[[பகுப்பு:")[1].strip().replace("]]","")
                    
                    if value != '-':
                        categories = categories + ' | '+value
                        
                    try:
                        value1 = i.split("[[பகுப்பு:")[2].strip().replace("]]","")
                        if value1 != '-':
                            categories = categories + ' | '+value1
                    except:
                        print "No Further Categories"
                    
                    try:
                        value2 = i.split("[[பகுப்பு:")[3].strip().replace("]]","")
                        if value2 != '-':
                            categories = categories + ' | '+ value2
                    except:
                        print "No Further Categories"
                
                    metaData[9] = categories.replace("|","",1).replace(" ","",2)

            #16 Content
            TOC = "-"

            try:
                if "Contents" in pageText:
                    contents = page.getWikiText().split("Contents}}==")[1].split("[[")[0].strip().replace("*","")
                    TOC = contents
            except:
                print "Not Found Contents"
                
            #15 Description
            description = "-"

            try:
                if "Description" in pageText:
                    desc = page.getWikiText().split("Description }}==")[1].split("[[")[0].strip();
                    description = desc
            except:
                print "Not Found"
        
            try:
                if "Description" in pageText:
                    desc = page.getWikiText().split("Description}}==")[1].split("==")[0].strip()
                    description = desc
                    #print description
            except:
                print "Not Found"

            metaData[11] = description
        
            metaData[12] = TOC
        
                # Appending rows to the Data Frame
            df = df.append({'ஆவண வகை':metaData[0] ,'அடையாளம்காட்டி': metaData[1], 'தலைப்பு': metaData[2],'ஆக்கர்':metaData[3], 'பதிப்பகர்': metaData[4], 'பதிப்புத்_திகதி':metaData[5], 'பதிப்பு':metaData[6], 'மொழி':metaData[7], 'வகை':metaData[8], 'துறை':metaData[9],'அளவு':metaData[10], 'விபரிப்பு': metaData[11], 'பொருளடக்கம்': metaData[12], 'பதிப்பாசிரியர்': metaData[13], 'வெளியீடு': metaData[14],'சுழற்சி':metaData[15], 'Full Text': pageText}, ignore_index=True)        
            
        except:
            missedDf = missedDf.append({'பெயர்':pagename},ignore_index=True)
            continue
            
    # Drfining the Columns to reindex
    columnsTitles = ['அடையாளம்காட்டி','தலைப்பு','ஆக்கர்','பதிப்பாசிரியர்','பதிப்பகர்','பதிப்புத்_திகதி','பதிப்பு','வெளியீடு','சுழற்சி','மொழி','வகை','துறை','அளவு','விபரிப்பு','ஆவண வகை','பொருளடக்கம்', 'Full Text']

    df = df.reindex(columns=columnsTitles)

    # exporting the DataFrame to CSV file
    export_csv = df.to_csv (r'metaData.csv', index = None, header=True, encoding = 'utf-8')

    #exporting wrong detailed articles
    missedDf.to_csv('missedFiles.csv', index=None, header=True, encoding = 'utf-8')
