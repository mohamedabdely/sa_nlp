import requests
from bs4 import BeautifulSoup
from dateutil import parser
from tqdm import tqdm
import mysql.connector as mysql
from urllib.parse import unquote
from datetime import datetime

db = mysql.connect(
    host = "localhost",
    port = 3307, 
    user = "root",
    passwd = "root", # MAMP SERVER
    database = "news"
)
cursor = db.cursor()
if(cursor):
    print("CONNECTED SUCCESSFULLY TO DB !")

# SELECTING FIRST ROW FROM DB
print("\nSELECTING DATA FROM DB...")
query = "SELECT * FROM urls WHERE nom_site = 'Alchourouk'"
# 11: National || 22: Economie || 33: Régional || 44: Politique || 55: Technolgie || 66: Culture || 77: International
cursor.execute(query)
all_urls = cursor.fetchall()
# SELECTING ALL LINKS FROM DB
print("\nSELECTING ALL LINKS FROM DB...")
query = "SELECT link_final FROM news WHERE source = 'Alchourouk'"
cursor.execute(query)
existed_links = cursor.fetchall()

def main():
    for url in all_urls:
        print("Category: ",url[4])
        for i in tqdm(range(101,201)):
            response = requests.get(f"{url[1]}?page={i}")
            soup = BeautifulSoup(response.text, 'html.parser')

            titles = soup.select('.row-article.views-row .views-field-title a')
            links = soup.select('.row-article.views-row .views-field-title a')
            dates = soup.select('.row-article.views-row .views-field-created span')
            descriptions = soup.select('.row-article.views-row .views-field-body')
            images = soup.select('.row-article.views-row .views-field-field-image img')
            
            for i in range(len(titles)):
                link = unquote("https://www.alchourouk.com" + links[i]['href'])

                if not existed_links or link not in [l[0] for l in existed_links]:
                    title = titles[i].text

                    if(descriptions[i].text.strip()):
                        description = descriptions[i].text
                    else:
                        description = title

                    date = dates[i].text
                    time_part, date_part = date.split(' - ')
                    formatted_date = parser.parse(date_part + ' ' + time_part)

                    image_src = "https://www.alchourouk.com" + images[i]['src']
                    image_name = image_src.split('/')[-1]

                    try:
                        query = "INSERT INTO test_news (source, national, datetime, titre, sub_content, link_final, path_image, name_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                        values = (url[3], url[4], formatted_date, title, description, link, image_src, image_name)
                        cursor.execute(query, values)
                        db.commit()
                    except Exception :
                        pass
                        

        now = datetime.now()
        sql_update2 = "UPDATE urls SET last_scraping='%s' where url='%s'" % (now,url[1])
        cursor.execute(sql_update2)
        db.commit()

    print("HAPPY SCRAPING :))) !")    

main()

"""
import mysql.connector as mysql

try:
    db = mysql.connect(
        host="localhost",
        port=3307,
        user="root",
        passwd="root",
        database="news"
    )
    if db.is_connected():
        print("✅ Connected successfully to 'news' database!")
except mysql.Error as e:
    print("❌ Error:", e)
"""