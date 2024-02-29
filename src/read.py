import pandas as pd
import os
import fitz 
import docx


def convert_docx_to_pdf(filename):
    os.system(f"unoconv -f pdf filename")


def read(path="source"):
    texts = []
    for filename in map(lambda x: path + "/" + x, os.listdir(path)):
        dot_ix = filename.rindex(".")
        name = filename[:dot_ix]
        extension = filename[dot_ix + 1:]
        if extension in ("doc", "docx"):
            convert_docx_to_pdf(filename)
        for block in process_docx_file(name + ".pdf"):
            texts.append((filename, block))
    return pd.DataFrame(texts, columns=["Filename", "Text"])


def process_pdf_file(filename):
    """Получает весь текст из pdf"""
    doc = fitz.open(filename)
    blocks = []
    for page in doc:
        for block in page.get_text_blocks():
            if block[4].startswith("<image:"):
                continue
            blocks.append(block[4])
    return blocks


def process_docx_file(filename):
    """Получает весь текст из docx"""
    doc = docx.Document(filename)
    return "\n".join([i.text for i in doc.paragraphs])


if __name__ == "__main__":
    df = read()
    df.to_csv("csv/text.csv", escapechar="\\")