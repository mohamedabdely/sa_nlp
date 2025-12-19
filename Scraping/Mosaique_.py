import requests
from dateutil import parser
from tqdm import tqdm
import mysql.connector as mysql
from urllib.parse import unquote
from datetime import datetime

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "root", # MAMP SERVER
    database = "news"
)

cursor = db.cursor()
if(cursor):
    print("CONNECTED SUCCESSFULLY TO DB !")

# SELECTING FIRST ROW FROM DB
print("\nSELECTING DATA FROM DB...")
query = "SELECT * FROM urls WHERE nom_site = 'Mosaique'"  
# 1: National || 2: Economie || 3: Régional || 4: Politique || 5: Technolgie || 7: International
cursor.execute(query)
all_urls = cursor.fetchall()
# SELECTING ALL LINKS FROM DB
print("\nSELECTING ALL LINKS FROM DB...")
query = "SELECT link_final FROM news WHERE source = 'Mosaique'"
cursor.execute(query)
existed_links = cursor.fetchall()
#part1, part2 = all_urls[0][2].split('page')
#url = f'{part1}ahahahha{part2}'

def main():
    for url in all_urls:
        print("Category: ", url[4])
        for i in tqdm(range(1,101)):
            part1, part2 = url[2].split('page')
            api_url = f"{part1}{i}{part2}"
            response = requests.get(api_url)
            target = response.json()
            items = target.get('items')

            for item in items:
                link = "https://www.mosaiquefm.net" + item.get('link')
                if not existed_links or link not in [unquote(l[0]) for l in existed_links]:
                    title = item.get('title')
                    date = parser.parse(item.get('startPublish').get('date'))
                    image_path = item.get('image')  
                    image_name = image_path.split('/')[-1] 
                    
                    query = "INSERT INTO news (source, national,datetime,titre,sub_content,link_final,path_image,name_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (url[3],url[4],date,title,title,link,image_path,image_name)
                    cursor.execute(query, values)
                    db.commit()

        now = datetime.now()
        sql_update2 = "UPDATE urls SET last_scraping='%s' where url='%s'" % (now,url[2])
        cursor.execute(sql_update2)
        db.commit()
        print("HAPPY SCRAPING :))) !")

main() 

