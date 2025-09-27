# exporter.py
from docx import Document
import os

def save_txt(path, text):
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def save_docx(path, text):
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)
    doc = Document()
    doc.add_paragraph(text)
    doc.save(path)
