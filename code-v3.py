#Import mandatory libraries 
import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import time
from unidecode import unidecode

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
      print(instagram_page)
      instagram_account = instagram_page.split('instagram.com/')[1].split('/', 1)[0]
      return unidecode(instagram_account)

    return error_instagram

  except: 
    return error


def get_follower_count(instagram_account):
  try:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"}
    r = requests.get('https://www.instagram.com/' + instagram_account, headers=headers, timeout=5)

    if r.status_code == 429:
      print(r.status_code)
      return -1

    if r.status_code != 200:
      print(r.status_code)
      return -1

    soup = BeautifulSoup(r.content, features="html.parser")
    followers = soup.find('meta', {'name': 'description'})['content']
    follower_count = followers.split('Followers')[0]
    follower_count = follower_count.replace('K', '000').replace('M', '000000').replace(',','').replace('.','')
    return int(follower_count)

  except: 
    return -1


def get_follower_count2(instagram_account):
  try:
    url = 'https://i.instagram.com/api/v1/users/web_profile_info/?username=' + instagram_account
    
    headers = {"User-Agent": "Instagram 76.0.0.15.395 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US; 138226743)"}
    r = requests.get(url, headers=headers, timeout=5)
    if r.status_code != 200: 
      print(r.status_code)
      return -1

    # f = open(instagram_account + ".html", "w")
    # f.write(r.content)
    # f.close
    
    json_data = r.json()
    return json_data["data"]["user"]["edge_followed_by"]["count"]
  except: 
    return -1


def get_last_row_number():
  try: 
    with open("modelo3.csv", 'r') as fread:
      for count, line in enumerate(fread):
          pass
    fread.close();

    print('last_row', count)
    
    return count
  except:
    return 0


#Read website list, get website name, and rename column label 
data = pd.read_csv('vtex.txt', sep=' ', header=None, names=["Site"])
sites = data['Site'];

last_row = get_last_row_number()

fieldnames = ["Site", "Instagram", "Seguidores", "Data"]
f = open("modelo3.csv", "a")
writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator = '\n')

followers_errors_count = 0
row = 0
for site in sites:
  row += 1

  if row <= last_row:
    continue

  print(str(row) + ' - ' + site);

  instagram_account = get_instagram_account(site)
  
  #tentar com o www
  if instagram_account == error_domain or instagram_account == error:
    instagram_account = get_instagram_account("www." + site);

  if "ERROR" in instagram_account:
    print(str(row) +' - ' + site + ' - ' + instagram_account + ' - ' + '-1' + ' - ' + datetime.now().strftime("%H:%M:%S"));
    writer.writerow({"Site": site , "Instagram": instagram_account, "Seguidores": -1, "Data": datetime.now().strftime("%H:%M:%S")})
    continue
  
  follower_count = get_follower_count(instagram_account)

  # verifica se o instagram bloqueou
  if follower_count == -1:
    followers_errors_count += 1
  else:
    followers_errors_count = 0

  if followers_errors_count > 2:
    f.close()
    exit()
  # --

  #print(f'{count} - {site} - {instagram_account} - {follower_count} - {datetime.now().strftime("%H:%M:%S")}');
  print(str(row) +' - ' + site + ' - ' + instagram_account + ' - ' + str(follower_count) + ' - ' + datetime.now().strftime("%H:%M:%S"))
  writer.writerow({"Site": site , "Instagram": instagram_account, "Seguidores": follower_count, "Data": datetime.now().strftime("%H:%M:%S")})

  f.close()
  f = open("modelo3.csv", "a")
  writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator = '\n')

  time.sleep(15)
  
f.close()   