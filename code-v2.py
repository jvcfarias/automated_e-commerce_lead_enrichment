#Import mandatory libraries 
import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

def get_instagram_page(site):
  instagram_account = site.split('.')[0]
  return 'https://www.instagram.com/' + instagram_account;

def get_follower_count(instagram_page):
  try:
    r = requests.get(instagram_page)
    if r.status_code == 404:
      return -1

    soup = BeautifulSoup(r.content, features="html.parser")
    followers = soup.find('meta', {'name': 'description'})['content']
    follower_count = followers.split('Followers')[0]
    follower_count = follower_count.replace('K', '000').replace('M', '000000')
    return int(follower_count)

  except: 
    return -1

#Read website list, get website name, and rename column label 
data = pd.read_csv('vtex.txt', sep=' ', header=None, names=["Site"])
sites = data['Site'];

f = open("modelo2.csv", "w")
writer = csv.DictWriter(f, fieldnames=["Site", "Instagram", "Seguidores", "Data"])
writer.writeheader()

for site in sites[:10]:
  print(site)
  instagram_page = get_instagram_page(site)
  follower_count = get_follower_count(instagram_page)
  writer.writerow({"Site": site , "Instagram": instagram_page, "Seguidores": follower_count, "Data": datetime.now().strftime("%H:%M:%S")})
  
f.close()   