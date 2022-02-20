from PyPDF2 import PdfFileReader, PdfFileWriter
import glob
import os
import re
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar,LTLine,LAParams
import os

list_of_pdf=glob.glob("*.pdf")
paper_title=[]
list_of_titles =[]
Extract_Data=[]
new_name=[]
old_name=[]
for i in range(len(list_of_pdf)):    
    try:
        pdfFileObj = open(list_of_pdf[i], 'rb')
        path=os.getcwd()+'\\'+list_of_pdf[i]
        pdfReader = PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getDocumentInfo()
        if pageObj.title==None or len(pageObj.title)==0  or len(pageObj.title)<=20:      
            for page_layout in extract_pages(path, page_numbers=[0,1]):
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        for text_line in element:
                            for character in text_line:
                                if isinstance(character, LTChar):
                                    Font_size=character.size
                        if Font_size>=12 and Font_size<=24 and len(element.get_text()) > 40 and len(element.get_text()) < 300:
                            Extract_Data.append([list_of_pdf[i],(element.get_text())])

        else:
            
            Extract_Data.append([list_of_pdf[i],pageObj.title])
            #print(Extract_Data[i])
        

    except :
            print(i,'PDF encrypted',path)  
            
    pdfFileObj.close()

for j in range(len(Extract_Data)):
    for k in str(Extract_Data[j][1]).split("fff"):
        paper_title.append([Extract_Data[j][0],re.sub(r"[-()\"#/@;:<>{}`+=~|.!?&\n]", " ", k)])    

number_of_renamed_files=0
number_of_renamed_files=0
files_to_be_renamed=[]
for n in range(len(paper_title)):
    try:
        old_name=os.getcwd()+'\\'+str(paper_title[n][0])
        new_name = os.getcwd()+'\\'+str(paper_title[n][1])+'.pdf'
        os.rename(old_name, new_name)
        number_of_renamed_files+=1
    except:
        #print(paper_title[n][0], paper_title[n][1], 'not named')     
        filed_to_rename+=1
        files_to_be_renamed.append([paper_title[n][0],paper_title[n][1]])
print("Rate of renaming files ",number_of_renamed_files/len(paper_title))