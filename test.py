import json
import datetime
import os

with open("cinestar_program_data.json", "r", encoding="utf8") as f:
    data = json.load(f)

cinemas_all = []
for item in data:
    cinemas_all.append({'cinema_name3':item['cinema_name3'], 'cinema_id':item['cinema_id']})
cinemas = []
for cinema in cinemas_all:
    if cinema not in cinemas:
        cinemas.append(cinema)

#print(data[0].values())
#print(cinemas)
for cinema in cinemas:
    print(cinema['cinema_name3'], cinema['cinema_id'])

last_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime("cinestar_program_data.json"))
print(f"The file was last modified on: {last_modified_time}")
print(last_modified_time)
print(datetime.datetime.now())
print(datetime.datetime.now()-last_modified_time)
print((datetime.datetime.now()-last_modified_time).total_seconds())
if (datetime.datetime.now()-last_modified_time).total_seconds()>350:
    print("yess")