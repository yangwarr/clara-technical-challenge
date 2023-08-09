import json
import requests
import csv 
import time 
import hashlib

try:
    with open("credentials.json", "r") as f:
        credentials = json.load(f)
except IOError as e:
    print("An error has occurred when opening the file credentials.json: ", e)

PUBLIC_KEY = credentials["PUBLIC_KEY"]
PRIVATE_KEY = credentials["PRIVATE_KEY"]
BASE_URL_COMICS = "http://gateway.marvel.com/v1/public/comics"
BASE_URL_CHARACTER = "http://gateway.marvel.com/v1/public/characters"
TS = str(int(time.time())) # creating a varying long string to use in the request
HASH_STRING = hashlib.md5(f"{TS}{PRIVATE_KEY}{PUBLIC_KEY}".encode('utf-8')).hexdigest() # https://docs.python.org/3/library/hashlib.html

def get_thor_id():

    params = { # https://developer.marvel.com/documentation/authorization
        "ts": TS,
        "apikey": PUBLIC_KEY,
        "hash": HASH_STRING,
        "name": "Thor"
    }

    request_response = requests.get(BASE_URL_CHARACTER, params=params) # http://gateway.marvel.com/v1/public/characters?ts=1691526362&apikey=e670eac043fe116db2cddb785a548e0c&hash=aa1bf6b766d531205fd74ef6be4ba491&name=Thor

    if request_response.status_code != 200: 
        print(request_response.raise_for_status())
    else:
        data = request_response.json()
        character = data["data"]["results"] # put all the relevant data into an object
        return character[0]["id"]

def main():

    #THOR_CHARACTER_ID = get_thor_id()

    params = { 
        "ts": TS,
        "apikey": PUBLIC_KEY,
        "hash": HASH_STRING,
        "characters": get_thor_id()
    }

    request_response = requests.get(BASE_URL_COMICS, params=params) # http://gateway.marvel.com/v1/public/comics?ts=1691526557&apikey=e670eac043fe116db2cddb785a548e0c&hash=b342b8e775d2e7f8bb50173a1bd986f1&characters=1009664

    if request_response.status_code != 200:
        print(request_response.raise_for_status())
    else:
        data = request_response.json()
        comics = data["data"]["results"] # put all the relevant data into an object
        
        csv_data = []
        for comic in comics: 
            title = comic["title"] # get title of the comic
            publication_year = comic["dates"][0]["date"][:4] # get only year of a date in YYYY-MM-DD format
            cover_url = comic["thumbnail"]["path"] + "/portrait_uncanny." + comic["thumbnail"]["extension"]  # path + image size + image extension
            csv_data.append([title, publication_year, cover_url])

        try:
            with open("thor_comics.csv", "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerows(csv_data)
            print("CSV file successfully generated.")      
        except IOError as e:
            print("An error occurred when writing to the file thor_comics.csv: ", e)        

if __name__ == "__main__":
    main()