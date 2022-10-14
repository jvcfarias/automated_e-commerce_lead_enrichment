#Import mandatory libraries 
import pandas as pd
import requests
from bs4 import BeautifulSoup

r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=(('user', 'pass')))

#Read website list, get website name, and rename column label 
data = pd.read_csv('vtex.txt', sep=' ', header=None, names=["Site"])
pages = data['Site'].str.split('.', expand=True)
pages = pages.rename({0:'Nome do site'}, axis=1)

#Number of instagram followers
for page in pages['Nome do site']:
    page_instagram = 'https://www.instagram.com/' + page
    print(page_instagram)
    r = requests.get(page_instagram)
    soup = BeautifulSoup(r.content)
    followers = soup.find('meta', {'name': 'description'})['content']
    follower_count = followers.split('Followers')[0]
    print(follower_count)
    break