import requests
from bs4 import BeautifulSoup
import os

def get_webpage(url):
    """Fetches the content of a webpage given its URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return None

def extract_pdf_links(html):
    """Parses the HTML content and extracts all PDF links."""
    soup = BeautifulSoup(html, 'html.parser')
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            pdf_links.append(href)
    return pdf_links

def download_pdf(url, save_path):
    """Downloads a PDF file from the given URL and saves it to the specified path."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  
        with open(filename, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")

if __name__ == "__main__":
    url = "https://fi-ing.unison.mx/acuerdos-de-sesiones-del-h-colegio-de-la-facultad-interdisciplinaria-de-ingenieria-2026/"
    html = get_webpage(url)
    if not html:
        print(f"Failed to retrieve the webpage: {url}")
        exit(1)
    pdf_links = extract_pdf_links(html)
    for link in pdf_links:
        print(link)
        filename = link.split('/')[-1]
        download_pdf(link, f"pdf_{filename}")
        print(f"Downloaded: {filename}")