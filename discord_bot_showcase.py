import discord
from discord.ext import commands
import os
import json
import subprocess
import datetime

class DaySelect(discord.ui.Select):
  def __init__(self, cinema_ids, movie_titles, options):
    self.cinema_ids = cinema_ids
    self.movie_titles = movie_titles
    #super().__init__(placeholder="Vyber den", min_values=1, max_values=len(options), options=options)
    super().__init__(placeholder="Vyber den", options=options)

  async def callback(self, interaction: discord.Interaction):
    #await interaction.response.send_message(content=f'You picked {self.cinema_ids} and {self.movie_titles} and {self.values}')
    with open("cinestar_program_data.json", "r", encoding="utf8") as f:
      data = json.load(f)
    data = [d for d in data if (d.get("cinema_id") in self.cinema_ids and d.get("movie_title") in self.movie_titles and d.get("date_id") in self.values)]
    
    embed = discord.Embed(description=data[0]['date'])
    embed.set_author(name=f"{data[0]['movie_title']} ({data[0]['length']})", url=data[0]['movie_url'])
    embed.set_thumbnail(url=data[0]['movie_img'])
    for item in data:
      embed.add_field(name=f"{item['time_start']}", value=f"[{item['movie_title_long']}]({item['time_url']}) · {item['time_end']}", inline=False)
    embed.set_footer(text=f"{data[0]['cinema_name3']} · {data[0]['date']}")
    
    await interaction.response.send_message(embed=embed)

class DaySelectView(discord.ui.View):
  def __init__(self, cinema_ids, movie_titles, options):
    super().__init__()
    self.add_item(DaySelect(cinema_ids, movie_titles, options))

class MovieSelect(discord.ui.Select):
  def __init__(self, cinema_ids, options):
    self.cinema_ids = cinema_ids
    #super().__init__(placeholder="Vyber film", min_values=1, max_values=len(options), options=options)
    super().__init__(placeholder="Vyber film", options=options)

  async def callback(self, interaction: discord.Interaction):
    with open("cinestar_program_data.json", "r", encoding="utf8") as f:
      data = json.load(f)
    data = [d for d in data if (d.get("cinema_id") in self.cinema_ids and d.get("movie_title") in self.values)]
    days_all = []
    for item in data:
      days_all.append({'date':item['date'], 'date_id':item['date_id']})
    days = []
    for day in days_all:
      if day not in days:
        days.append(day)
    
    options_days = []
    for day in days:
      options_days.append(discord.SelectOption(label=day['date'], value=day['date_id']))
    await interaction.response.send_message(content="Jaký den chceš vyrazit?", view=DaySelectView(self.cinema_ids, self.values, options_days))

class MovieSelectView(discord.ui.View):
  def __init__(self, cinema_ids, options):
    super().__init__()
    self.add_item(MovieSelect(cinema_ids, options))

class CinemaSelect(discord.ui.Select):
  def __init__(self, options):
    #super().__init__(placeholder="Vyber kino", min_values=1, max_values=len(options), options=options)
    super().__init__(placeholder="Vyber kino", options=options)

  async def callback(self, interaction: discord.Interaction):
    with open("cinestar_program_data.json", "r", encoding="utf8") as f:
      data = json.load(f)
    data = [d for d in data if d.get("cinema_id") in self.values]
    movies_all = []
    for item in data:
      movies_all.append({'movie_title':item['movie_title']})
    movies = []
    for movie in movies_all:
      if movie not in movies:
        movies.append(movie)
    
    options_movies = []
    for movie in movies:
      options_movies.append(discord.SelectOption(label=movie['movie_title']))
    await interaction.response.send_message(content="Na co to bude?", view=MovieSelectView(self.values, options_movies))

class CinemaSelectView(discord.ui.View):
  def __init__(self, options):
    super().__init__()
    self.add_item(CinemaSelect(options))

class Client(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())

  async def on_ready(self):
    #await tree.sync(guild=discord.Object(id=os.environ['DISCORD_SERVER_ID']))
    #self.synced = True
    await self.tree.sync(guild=discord.Object(id=os.environ['DISCORD_SERVER_ID']))
    print('We have logged in!')

client = Client()

@client.tree.command(name="cinema", description="Pick a cinema movie", guild=discord.Object(id=os.environ['DISCORD_SERVER_ID']))
async def cinema(interaction: discord.Interaction):
  with open("cinestar_program_data.json", "r", encoding="utf8") as f:
    data = json.load(f)
  cinemas_all = []
  for item in data:
    cinemas_all.append({'cinema_name3':item['cinema_name3'], 'cinema_id':item['cinema_id']})
  cinemas = []
  for cinema in cinemas_all:
    if cinema not in cinemas:
      cinemas.append(cinema)
    
  options = []
  for cinema in cinemas:
    options.append(discord.SelectOption(label=cinema['cinema_name3'], value=cinema['cinema_id']))
    
  await interaction.response.send_message(content="Tak kampak se vydáme?", view=CinemaSelectView(options))

@client.tree.command(name="scrape", description="scrape cinestar", guild=discord.Object(id=os.environ['DISCORD_SERVER_ID']))
async def scrape(interation: discord.Interaction):
  last_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime("cinestar_program_data.json"))
  if (datetime.datetime.now()-last_modified_time).total_seconds()>300:
    subprocess.call(['python', 'cinema_scraper_project/crawl.py'])
  else:
    await interation.response.send_message(f"Data nejsou starší než 5 minut. Počkej ještě {int(300-(datetime.datetime.now()-last_modified_time).total_seconds())} vteřin.")


client.run(os.environ['TOKEN'])
