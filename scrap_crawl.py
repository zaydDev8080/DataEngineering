import requests
import pymongo
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

myclient = pymongo.MongoClient("mongodb://AdminZ:AdminPWD@cluster0-shard-00-00-gfv3w.mongodb.net:27017,cluster0-shard-00-01-gfv3w.mongodb.net:27017,cluster0-shard-00-02-gfv3w.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

db = myclient.test
print("Mongo DataBase:",db)
mydb = myclient["ScrapedDB"]
mycol = mydb["ScrapedData"]

response = requests.get('http://www.bbc.co.uk/news')
doc = BeautifulSoup(response.text, 'html.parser')

news = doc.find_all('div', { 'class': 'gs-c-promo' })
for Article in news:
        print("THIS IS A STORY")
        headline = Article.find('h3')
        print(headline.text)
        link = Article.find('a')
        if ("www.bbc.co" not in link['href']):
            fullLink = "http://www.bbc.co.uk" + link['href']
        else:
            fullLink = link['href']

        if (not Article.find('p')):
            summary = ""
        else:
            summary = Article.find('p').text

        site_Article = fullLink
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site_Article, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, 'html.parser')

        sub_news = soup.find_all('span', {'class': 'image-and-copyright-container'})

        for sub_Article in sub_news:
            imageTag = sub_Article.find('img', {'class': "js-image-replace"})
            if (not imageTag):
                 image="Empty"
            else: image = imageTag['src']
        print(image)

        print(summary)
        ScrapedDoc1 = {"headline": headline.text, "link": fullLink, "summary": summary, "Image": image }
        InsertDoc = mycol.insert_one(ScrapedDoc1)
        print("--------------------inserted-------------------")
        print("----------------", InsertDoc.inserted_id, "---------------")
        print("------------------------------------------------")


print("-- Done --")



