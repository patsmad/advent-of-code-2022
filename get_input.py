import requests
import json

with open('headers.json', 'r') as f:
    headers = json.load(f)

def get_input(day, strip=True):
    if strip:
        return requests.get('https://adventofcode.com/2022/day/{}/input'.format(day), headers=headers).text.strip()
    else:
        return requests.get('https://adventofcode.com/2022/day/{}/input'.format(day), headers=headers).text
