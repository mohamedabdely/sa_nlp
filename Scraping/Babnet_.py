from bs4 import BeautifulSoup
import requests
import dateparser
import mysql.connector as mysql
from datetime import datetime
from tqdm import tqdm

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
query = "SELECT * FROM urls where nom_site ='Babnet' "
cursor.execute(query)
all_urls = cursor.fetchall()

# SELECTING ALL LINKS FROM DB
print("\nSELECTING ALL LINKS FROM DB...")
query = "SELECT link_final FROM news WHERE source = 'Babnet'"
cursor.execute(query)
existed_links = cursor.fetchall()


def main():
    for url in all_urls:
        print("\nCat: ", url[4])
        for i in tqdm(range(1, 3100, 30)):
            res = requests.get(f'{url[1]}?p={i}')
            soup = BeautifulSoup(res.text, 'html.parser') 
            
            titles = soup.select('h2.post-title.title-large.arabi a')
            dates = soup.select('span.post-date')

            for i in range(len(titles)):
                link = ("https://www.babnet.net/" + titles[i]['href'])
                if not existed_links or link not in [l[0] for l in existed_links]:
                    title = titles[i].text.strip()
                    date = dateparser.parse(dates[i].text.strip(), languages=['fr'])
                    
                    response = requests.get(link)
                    soup1 = BeautifulSoup(response.text, 'html.parser')

                    image_path = "https://www.babnet.net" + soup1.select_one('div.post-media.post-featured-image.text-center img')['src']
                    image_name = image_path.split('/')[-1]

                    target = soup1.select('div#smile div.box')[0]
                    for br in target.find_all("br"):
                        br.replace_with("")
                    description = target.get_text(strip=True, separator='')

                    try:
                        query = "INSERT INTO news (source, national, datetime, titre, sub_content, link_final, path_image, name_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                        values = (url[3], url[4], date, title, description, link, image_path, image_name)
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

'''
    url = "https://www.babnet.net/sport.php?p=1"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    titles = soup.select('h2.post-title.title-large.arabi a')
    dates = soup.select('span.post-date')

    for i in range(len(dates)):

        title = titles[i].text.strip()
        date = dateparser.parse(dates[i].text.strip(), languages=['fr'])
        link = "https://www.babnet.net/" + titles[i]['href']

        response = requests.get(link)
        soup1 = BeautifulSoup(response.text, 'html.parser')

        image_path = "https://www.babnet.net" + soup1.select_one('div.post-media.post-featured-image.text-center img')['src']
        image_name = image_path.split('/')[-1]
        print(image_name)
        target = soup1.select('div#smile div.box')[0]
        for br in target.find_all("br"):
            br.replace_with("")
        description = target.get_text(strip=True, separator='')
        # Query
        query = "INSERT INTO news (source, national,datetime,titre,sub_content,link_final,path_image,name_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = ("Mosaique",'National',date,title,title,link,image_path,image_name)
        cursor.execute(query, values)
        db.commit()
'''