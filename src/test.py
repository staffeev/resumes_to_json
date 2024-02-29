from pyresparser import ResumeParser

data = ResumeParser('../source/Akhundov Damat').get_extracted_data()
print(data)