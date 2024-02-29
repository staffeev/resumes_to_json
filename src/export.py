import pandas as pd
from read import read
import json

def get_contact_Items(df_row, data: dict, index):
    contact_items = ["Phone","Email","Skype","Telegram","Github"]
    for id, contact_item in enumerate(contact_items):
        if contact_item in df_row:
            contact_dict = {
                "resume_contact_item_id": id,
                "value": df_row[contact_item],
                "comment": None,
                "contact_type": contact_item
            }
            element = data[f"resume{index}"]["contactItems"]
            element.append(contact_dict)
            data[f"resume{index}"]["contactItems"] = element

def get_education_Items():
    pass

def get_expirience_Items():
    pass

def get_language_Items():
    pass

def export(df):
    for index, row in df.iterrows():
        data = {
            f"resume{index}":{
                "resume_id": index,
                "first_name": row["NameSurname"][0] if ("NameSurname" in row) and (not row["NameSurname"] is None) else None,
                "last_name": row["NameSurname"][1] if ("NameSurname" in row) and (not row["NameSurname"] is None) else None,
                "birth_date": None,
                "birth_date_year_only": None,
                "country": row["Country"] if "Country" in row else None,
                "city": row["City"] if "City" in row else None,
                "about": None,
                "key_skills": None,
                "salary_expectation_amount": None,
                "salary_expectation_currency": None,
                "photo_path": None,
                "gender": None,
                "resume_name": row["Filename"],
                "source_link": None,
                "contactItems": [],
                "educationItems": [],
                "exxperienceItems": [],
                "languageItems": []
            }
        }
        get_contact_Items(row, data, index)
        get_education_Items()
        get_expirience_Items()
        get_language_Items()
        with open("src/json_test/test.json","a") as f:
            f.write(json.dumps(data, indent=4)) 