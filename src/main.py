# from pipeline import Pipeline

# p = Pipeline()
# p.run_all()
import os
print(os.curdir)
import aspose.words as aw
doc = aw.Document("isolator/Нурутдинов Александр.doc")
doc.save("random/Нурутдинов Александр.pdf")

from docx2pdf import convert
 
convert("/isolator/Alina Borovik.docx", "/random/Alina Borovik.pdf")