#Import mandatory libraries 
import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

error_domain = "ERROR_DOMAIN"
error_instagram = "ERROR_INSTAGRAM"
error = "ERROR"

def get_instagram_account(site):
  try:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    r = requests.get("https://" + site, headers=headers, timeout=5)
    #print(r.status_code)

    if r.status_code != 200:
      return error_domain

    soup = BeautifulSoup(r.content, features="html.parser")
    elements = soup.select('[href*="instagram.com/"]')
    if elements:
      instagram_page = elements[0]['href']
      instagram_account = instagram_page.split('instagram.com/')[1].split('/', 1)[0]
      return instagram_account

    return error_instagram

  except: 
    return error


def get_follower_count(instagram_account):
  try:
    url = 'https://i.instagram.com/api/v1/users/web_profile_info/?username=' + instagram_account
    
    headers = {"User-Agent": "Instagram 76.0.0.15.395 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US; 138226743)"}
    r = requests.get(url, headers=headers, timeout=5)
    if r.status_code != 200:
      return -1
      
    json_data = r.json()
    return json_data["data"]["user"]["edge_followed_by"]["count"]
  except: 
    return -1


#Read website list, get website name, and rename column label 
data = pd.read_csv('vtex.txt', sep=' ', header=None, names=["Site"])
sites = data['Site'];

f = open("modelo3.csv", "w")
writer = csv.DictWriter(f, fieldnames=["Site", "Instagram", "Seguidores", "Data"])
writer.writeheader()

count = 0
for site in sites:
  count += 1
  print(str(count) + ' - ' + site);

  instagram_account = get_instagram_account(site)
  
  #tentar com o www
  if instagram_account == error_domain or instagram_account == error:
    instagram_account = get_instagram_account("www." + site);

  if "ERROR" in instagram_account:
    print(str(count) +' - ' + site + ' - ' + instagram_account + ' - ' + '-1' + ' - ' + datetime.now().strftime("%H:%M:%S"));
    writer.writerow({"Site": site , "Instagram": instagram_account, "Seguidores": -1, "Data": datetime.now().strftime("%H:%M:%S")})
    continue
  
  follower_count = get_follower_count(instagram_account)

  #print(f'{count} - {site} - {instagram_account} - {follower_count} - {datetime.now().strftime("%H:%M:%S")}');
  print(str(count) +' - ' + site + ' - ' + instagram_account + ' - ' + str(follower_count) + ' - ' + datetime.now().strftime("%H:%M:%S"));
  writer.writerow({"Site": site , "Instagram": instagram_account, "Seguidores": follower_count, "Data": datetime.now().strftime("%H:%M:%S")})
  
f.close()   