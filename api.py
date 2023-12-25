import requests
import json

r = requests.get('https://chart.googleapis.com/chart?cht=qr&chs=500x500&chl=he%E1%BA%BBtyuiop')

print(r.content.split(";"))