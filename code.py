#Import mandatory libraries 
import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup

r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=(('user', 'pass')))

#Read website list, get website name, and rename column label 
data = pd.read_csv('vtex.txt', sep=' ', header=None, names=["Site"])
pages = data['Site'].str.split('.', expand=True)
pages = pages.rename({0:'Nome do site'}, axis=1)

f = open("modelo2.csv", "w")
writer = csv.DictWriter(f, fieldnames=["Site", "Cliente", "Instagram", "Seguidores"])

#Number of instagram followers + exporting to csv
f = open("modelo2.csv", "w")
writer = csv.DictWriter(f, fieldnames=["Site", "Cliente", "Instagram", "Seguidores"])
writer.writeheader()
f = open("modelo2.csv", "w")
writer = csv.DictWriter(f, fieldnames=["Site", "Cliente", "Instagram", "Seguidores"])
writer.writeheader()
for page in pages['Nome do site']:
    page_instagram = 'https://www.instagram.com/' + page
    r = requests.get(page_instagram)
    soup = BeautifulSoup(r.content, features="html.parser")
    try:
        followers = soup.find('meta', {'name': 'description'})['content']
        follower_count = followers.split('Followers')[0]
        follower_count = follower_count.replace('K', '000').replace('M', '000000')
        if int(follower_count) > 20000:
            writer.writerow({"Site": page + '.com.br' , "Cliente": page, "Instagram": page_instagram, "Seguidores": follower_count})
    except: 
        pass
f.close()   