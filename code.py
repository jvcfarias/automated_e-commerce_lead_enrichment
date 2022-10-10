#Import mandatory libraries 
import pandas as pd
import requests

#Read website list, get website name and try to find its instagram page
data = pd.read_csv('vtex.txt', sep=' ', header=None, names=["Site"])
page = data['Site'].str.split('.', expand=True)
instagram_page = 'https://www.instagram.com/' + page[0]

#Requesting number of followers with requests package python
instagram_request = requests.get(instagram_page).text
start = '"edge_followed_by":{"count":'
end = '}"'
followers = instagram_request[instagram_request.find(start)+len(start):instagram_request.rfind(end)]

print(followers)