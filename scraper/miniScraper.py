import requests
from bs4 import BeautifulSoup

def scrape():

    url = "https://registroapps.uniandes.edu.co/scripts/semestre/adm_con_horario1_joomla.php?depto=LENG&nombreDepto=Lenguas%20y%20Cultura"
    s = requests.Session()
    response = s.get(url)
    response.encoding = 'utf-8'
    page = response.text

    soup = BeautifulSoup(page, 'html5lib');

    for tag in soup.findAll(findValidTables):
        a = 3

def findValidTables(tag):
    desc = len(list(tag.descendants))
    if tag.name == 'table':
        print( "Cellspacing: " + str(tag['cellspacing']) + " // Border: " + str(tag['border']) + " // Cellpadding: " + str(tag['cellpadding']) + " // Width: " + str(tag['width']) + " // Descendants: " + str(len(list(tag.descendants))))
        valid = False
        ''' if desc == 84:
            print("strange shit: ", tag) '''
        if desc == 25:
            print("??25: ", tag)
        if desc == 11:
            print("11??: ", tag)
    
        
    return tag.name == 'table' and tag['cellspacing'] == '1'and desc != 25 and desc != 11


scrape();