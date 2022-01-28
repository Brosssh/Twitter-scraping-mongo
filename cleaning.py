import itertools
import re
from datetime import datetime


def convert_datatime(stringa):
    return datetime.strptime(stringa, '%b %d, %Y,%I:%M %p').isoformat()

def clean_text(stringa):
    clean_data = {}
    clean_data['text'] = str(stringa)
    linklist=re.findall(r"(https?://[^\s]+)", stringa)
    if len(linklist)>0:
        clean_data['links'] = linklist
    hashlist = re.findall(r'#\w+', stringa)
    if len(hashlist)>0:
        clean_data['hashtags'] = hashlist
    taggedlist=re.findall(r'@\w+', stringa)
    if len(taggedlist) > 0:
        clean_data['tagged_users'] = taggedlist
    return clean_data

#4:23 PM · Jan 21, 2022 from Hounslow, London·Twitter for Android
def clean_date_source(stringa):
    print("Cleaning of the tweet... ")
    clean_data = {}
    try:
        data_temp = re.findall('·\s.+\s\d+(?=·)', stringa)[0][2:]
        data_temp += ','
        data_temp += re.findall('\d+:\d\d\s[AM|PM]+', stringa)[0]
        clean_data['date_time'] = convert_datatime(data_temp)
        clean_data['source'] = re.findall('·\w.+', stringa)[0][1:]
    except:
        print("TODO fixare questo errore")
    return clean_data

def clean_attachment(stringa):
    print("Cleaning attachment...")
    clean_data={}
    try:
        clean_data["author_alias"]= stringa.split("\n")[1]
        clean_data["author_name"] = stringa.split("\n")[2]
        clean_data["time_of_replying"] = stringa.split("\n")[3].split("· ")[1]
        clean_data={**clean_data, **clean_text(str("\n".join(stringa.split("\n")[4:])))}
        return clean_data
    except:
        print("Skipping attachment")