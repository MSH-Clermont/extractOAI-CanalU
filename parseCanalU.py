import requests
import csv
from bs4 import BeautifulSoup as bs
import string
import re

urlAppelMSHCanalU = "https://www.canal-u.tv/oai?verb=ListRecords&metadataPrefix=oai_dc&resumptionToken="

urlChaineMSH = "https://www.canal-u.tv/oai?verb=ListRecords&metadataPrefix=oai_dc&set=chaine:"


def convert_duration(iso_duration):
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
    if match:
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return None

def process_records(tousRecord):
    # Fonction pour traiter chaque enregistrement
    for eachRecord in tousRecord:
        # Vérifier si la citation bibliographique est présente
        if eachRecord.find("dc:bibliographicCitation"):
            citation = eachRecord.find("dc:bibliographicCitation").string 
        else:
            # Sinon, utiliser l'identifiant
            citation = eachRecord.find('dc:identifier').string
        # Récupérer la durée

        if eachRecord.find("dc:extent"):
            dureeOrigin = eachRecord.find("dc:extent").string
            # Appliquer les remplacements
            duree = convert_duration(dureeOrigin)
            print (duree)
        # Récupérer tous les sujets associés à l'enregistrement
        subjects = eachRecord.find_all('dc:subject')
        # Créer une liste des textes des sujets
        subject_texts = [subject.string for subject in subjects if subject.string]
        # Joindre les sujets en une seule chaîne , séparés par une virgule
        subject = ', '.join(subject_texts)
        # Écrire les données dans le fichier CSV
        writer.writerow(
            {fieldnames[0]: citation,
             fieldnames[1]: duree,
             fieldnames[2]: subject
            })


def call_API(token):
    # Construire l'URL pour l'appel à l'API avec le token de reprise (resumptionToken)
    url = urlAppelMSHCanalU + token
    response = requests.request("GET", url)

    # Récupérer le contenu de la réponse
    resultat = response.text
    soup = bs(resultat, "xml")

    # Récupérer toutes les balises 'record' dans la réponse
    tousRecord = soup.find_all('record')

    # Vérifier si un token de reprise est présent
    if soup.resumptionToken:
        # Récupération de la balise resumptionToken
        resumptionToken = soup.resumptionToken
        resumptionTokenValue = resumptionToken.string
        # Traiter les enregistrements récupérés
        process_records(tousRecord)
        # Appeler l'API avec le token de reprise pour récupérer plus de données
        call_API(resumptionTokenValue)
    else:
        # Si pas de token, traiter les enregistrements normalement
        process_records(tousRecord)


def call_MSHCanalU(idMSH):
    # Construire l'URL pour l'appel à l'API avec l'identifiant MSH
    url = urlChaineMSH + idMSH 
    response = requests.request("GET", url)

    # Récupérer le contenu de la réponse
    resultat = response.text
    soup = bs(resultat, "xml")

    # Récupérer toutes les balises 'record' dans la réponse
    tousRecord = soup.find_all('record')

    # Vérifier si un token de reprise est présent
    if soup.resumptionToken:
        # Récupération de la balise resumptionToken
        resumptionToken = soup.resumptionToken
        resumptionTokenValue = resumptionToken.string
        # Traiter les enregistrements récupérés
        process_records(tousRecord)
        # Appeler l'API avec le token de reprise pour récupérer plus de données
        call_API(resumptionTokenValue)
    else:
        # Si pas de token, traiter les enregistrements normalement
        process_records(tousRecord)


with open('data/allMetadataCanalU-MSH.csv', 'w', newline='') as csvfile:
    fieldnames = ['citation', 'duree', 'domaine_motsCles']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    call_MSHCanalU ("731")