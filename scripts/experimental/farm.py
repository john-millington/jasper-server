import requests
import sys
import time

with open('./symspell/dict.txt') as filein:
    lines = [line.rstrip('\n') for line in filein]
    found = False

    for line in lines:
        string = line.split(' ')[0]
        if (not found and string != sys.argv[1]):
            continue

        found = True
        requests.get('http://localhost:1000/api/analyse?q=' + string + '&count=100&fields=emotion,sentiment&sources=twitter')
        print(string)

        time.sleep(10)