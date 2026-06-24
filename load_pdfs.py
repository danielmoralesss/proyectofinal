import os
from pypdf import PdfReader
from models import db, Document
from app import app
from datetime import datetime

PDF_FOLDER = "PDF_SEARCH"

with app.app_context():

    print("📂 Buscando en carpeta:", os.path.abspath(PDF_FOLDER))

    files = os.listdir(PDF_FOLDER)
    print("📄 Archivos encontrados:", files)

    for filename in files:
        if filename.endswith(".pdf"):
            path = os.path.join(PDF_FOLDER, filename)

            print("✅ Procesando:", filename)

            reader = PdfReader(path)
            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

        doc = Document(
            url=filename,
            content=text if text.strip() else "PDF sin texto",
            year=datetime.now().year
        )

        db.session.add(doc)

if not text.strip():
    print("⚠️ PDF sin texto:", filename)

    db.session.commit()

print("✅ Proceso terminado")