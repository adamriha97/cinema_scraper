import json
import datetime
import os

with open("cinestar_program_data.json", "r", encoding="utf8") as f:
    data = json.load(f)

#data = [d for d in data if (d.get("cinema_id") in ['11'] and d.get("movie_title") in ['ONEMANSHOW: The Movie CZ'] and d.get("date_id") in ['2023-08-06'])]

data = [d for d in data if (d.get("movie_title_long") in ['ONEMANSHOW: The Movie CZ'])]

print(data)

for item in data:
    print(item['cinema_name3'], item['cinema_id'], item['movie_title_long'])
