# from pipeline import Pipeline

# p = Pipeline()
# p.run_all()


import os

s = os.listdir("source")
print(len([i for i in s if i.endswith(".doc") or i.endswith(".docx")]), len(s))