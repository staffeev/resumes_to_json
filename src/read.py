import pandas as pd
import os
import fitz 
import aspose.words as aw


def convert_docx_to_pdf(name, extension):
    doc = aw.Document(f"{name}.{extension}")
    doc.save(f"{name}.pdf")


def remove_tmp_files(filanames):
    [os.remove(name) for name in filanames]


def read(path="source", ignore_docx=True):
    texts = []
    tmp_files = []
    for filename in map(lambda x: path + "/" + x, os.listdir(path)):
        dot_ix = filename.rindex(".")
        name = filename[:dot_ix]
        extension = filename[dot_ix + 1:]
        if extension in ("doc", "docx"):
            if ignore_docx:
                continue
            convert_docx_to_pdf(name, extension)
            tmp_files.append(name + ".pdf")
        blocks, all_text = process_pdf_file(name + ".pdf")
        texts.append((filename, name + ".pdf", blocks, all_text))
    return tmp_files, pd.DataFrame(texts, columns=["Filename", "UsedFilename", "Blocks", "Text"])


def process_pdf_file(filename):
    """Получает весь текст из pdf"""
    doc = fitz.open(filename)
    blocks = []
    all_text = ""
    for page in doc:
        for block in page.get_text_blocks():
            if block[4].startswith("<image:") or "Aspose.Words" in block[4]:
                continue
            blocks.append(block[4])
            all_text += block[4] + "\n"
    return blocks, all_text


if __name__ == "__main__":
    _, df = read()
    df.to_csv("csv/text.csv", escapechar="\\")