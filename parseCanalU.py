import requests
import csv
from bs4 import BeautifulSoup as bs
import string
import re

urlAppelMSHCanalU = "https://www.canal-u.tv/oai?verb=ListRecords&metadataPrefix=oai_dc&resumptionToken="



def call_API(token):

    url=urlAppelMSHCanalU+token

    response = requests.request("GET", url)

    resultat = response.text

    soup = bs(resultat, "xml")

    #toutes les balises record
    tousRecord = soup.find_all('record')

    if soup.resumptionToken:
        #Récupération de la balise resumptionToken
        resumptionToken =soup.resumptionToken
        # récupérer la valeur  de la balise resumptionToken pour faire un deuxième appel oai
        resumptionTokenValue = resumptionToken.string
        
        for eachRecord in tousRecord:
            if eachRecord.find("dc:bibliographicCitation"):
                citation = eachRecord.find("dc:bibliographicCitation").string 
            else:
                citation = eachRecord.find('dc:identifier').string
            duree = eachRecord.find("dc:extent").string
            print(duree)
            subjects = eachRecord.find_all('dc:subject')
            subject_texts = [subject.string for subject in subjects if subject.string]
            # Vous pouvez ensuite les joindre en une seule chaîne si nécessaire
            subject = ', '.join(subject_texts)
            writer.writerow(
                            {fieldnames[0]: citation,
                            fieldnames[1]: duree,
                            fieldnames[2]: subject
                            })
        
        call_API(resumptionTokenValue)

    else:
         for eachRecord in tousRecord:
            if eachRecord.find("dc:bibliographicCitation"):
                citation = eachRecord.find("dc:bibliographicCitation").string 
            else:
                citation = eachRecord.find('dc:identifier').string
            duree = eachRecord.find("dc:extent").string
            print(duree)
            subjects = eachRecord.find_all('dc:subject')
            subject_texts = [subject.string for subject in subjects if subject.string]
            # Vous pouvez ensuite les joindre en une seule chaîne si nécessaire
            subject = ', '.join(subject_texts)
            writer.writerow(
                            {fieldnames[0]: citation,
                            fieldnames[1]: duree,
                            fieldnames[2]: subject
                            })
          
    return
    
with open('data/allMetadataCalaU.csv', 'w', newline='') as csvfile:
    fieldnames = ['citation', 'duree', 'domaine_motsCles']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    call_API ("cd655488-4d1b-440a-836b-93dc935ec102-1733243312")