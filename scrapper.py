import requests
from bs4 import BeautifulSoup

def get_related_urls(url, limit=2):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    related_urls = []

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('http') and len(related_urls) < limit:
            related_urls.append(href)
    
    return related_urls

def clean_text(soup):
    for script in soup(["script", "style"]):
        script.decompose()  # Enlever les balises non pertinentes

    text = soup.get_text(separator=" ")
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text

def scrape_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return clean_text(soup)

def scrapping_site(url):
    related_urls = get_related_urls(url)
    texts = []
    
    texts.append(scrape_text_from_url(url))
    for related_url in related_urls:
        texts.append(scrape_text_from_url(related_url))
    
    return texts
# # Utilisation
# url = "https://www.levaldespres.com/fr"
# texts = scrapping_site(url)
# # Store the result in a variable "scrapping"
# scrapping = ""
# for i, text in enumerate(texts):
#     scrapping += f"Texte de la page {i+1}: {text.strip()}\n"
