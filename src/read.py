import pandas as pd
import os
import fitz 
import docx


def read(path="source"):
    texts = []
    for filename in map(lambda x: path + "/" + x, os.listdir(path)):
        file_extension = filename[filename.rindex(".") + 1:]
        if file_extension == "pdf":
            texts.append((filename, process_pdf_file(filename)))
        elif file_extension in ("doc", "docx"):
            texts.append((filename, process_docx_file(filename)))
    return pd.DataFrame(texts, columns=["Filename", "Text"])


def process_pdf_file(filename):
    """Получает весь текст из pdf"""
    doc = fitz.open(filename)
    return "\n".join(["".join(page.get_text()) for page in doc])


def process_docx_file(filename):
    """Получает весь текст из docx"""
    doc = docx.Document(filename)
    return "\n".join([i.text for i in doc.paragraphs])


if __name__ == "__main__":
    df = read()
    df.to_csv("csv/text.csv", escapechar="\\")