import time
import requests
import webbrowser
import os
from datetime import datetime

url = "https://api.nasa.gov/planetary/apod"
api_key = "DEMO_KEY"

date_input = input("Donnez une date (dd-mm-yyyy) : \n").strip()
date = None

if date_input:
    try:
        date = datetime.strptime(date_input, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        date = None

images_folder = os.path.join(os.path.expanduser("~"), "Pictures", "APOD_Images")
os.makedirs(images_folder, exist_ok=True)

params = {"api_key": api_key}
if date:
    params["date"] = date

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    hdurl = data.get("hdurl")

    phrase = f"Téléchargement de l'image :, {hdurl} \n"
    print(phrase)

    if hdurl:
        image_response = requests.get(hdurl)

        if image_response.status_code == 200:
            date_str = date.replace("-", "") if date else datetime.now().strftime("%d_%m_%y")
            filename = f"APOD_{date_str}.jpg"
            file_path = os.path.join(images_folder, filename)

            with open(file_path, "wb") as file:
                file.write(image_response.content)

            print(f"Image {filename} téléchargée avec succès \n")
            print(f"Ouverture de l'image {filename} ")

            time.sleep(3)
            webbrowser.open(f"file://{file_path}")
