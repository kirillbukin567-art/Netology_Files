from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
with open('phonebook_raw.csv', encoding="UTF-8" ) as f:
    rows= csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

# ------------- TODO 1
header,data= contacts_list[0],contacts_list[1:]
def fix_name(row):
    parts = " ".join(row[:3]).split()
    parts+= [""] * (3-len(parts))
    row[:3]= parts[:3]
    return row
#Пункт 2:Телефоны
pattern_str: str = (
    r"(?:\+7|8)?[\s-]*"
    r"\(?(\d{3})\)?[\s-]*"
    r"(\d{3})[\s-]*"
    r"(\d{2})[\s-]*"
    r"(\d{2})"
    r"(?:\s*\(?доб\.?\s*(\d+)\)?)?"
)
phone_pattern = re.compile(pattern_str)
def fix_phone(phone):
    def repl(m):
        result = f"+7({m.group(1)}){m.group(2)}-{m.group(3)}-{m.group(4)}"
        if m.group(5):
            result+=f" доб.{m.group(5)}"
        return result
    return phone_pattern.sub(repl,phone)

def merge_duplicates(rows):
    merged={}
    for row in rows:
        key=(row[0],row[1])
        if key not in merged:
            merged[key]=row[:]
        else:
            for i,value in enumerate(row):
                if not merged[key][i] and value:
                    merged[key][i]=value
    return list(merged.values())

data = [fix_name(row) for row in data]
for row in data:
    row[5]= fix_phone(row[5])
data=merge_duplicates(data)
contacts_list = [header]+data
pprint(contacts_list)

#-------- TODO 2:сохраняем результат
with open("phonebook.csv" , "w", encoding="UTF-8", newline="") as f:
    datawriter=csv.writer(f,delimiter=",")
    datawriter.writerows(contacts_list)            
