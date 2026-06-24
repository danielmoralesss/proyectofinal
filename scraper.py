import requests
from bs4 import BeautifulSoup
from models import db, Document
from datetime import datetime

def scrape_url(url_obj):
    try:
        # Hacer petición HTTP
        response = requests.get(url_obj.link)

        # Analizar HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Obtener todos los párrafos
        paragraphs = soup.find_all("p")

        # Unir texto
        text = "\n".join([p.get_text() for p in paragraphs])

        # Crear documento en la base de datos
        doc = Document(
            url=url_obj.link,
            content=text,
            year=datetime.now().year
        )

        db.session.add(doc)
        db.session.commit()

    except Exception as e:
        print("Error scraping:", e)