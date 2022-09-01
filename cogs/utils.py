from discord import member, Color, Embed
from dateutil import parser
from math import ceil
import requests
import config

def search_manga_embed(results, total, query):
    current_results = len(results)
    loops = (total - current_results) / 8
    loops = ceil(loops)
    embeds = []
    initial_embed = Embed()
    initial_embed.color = 0x52b9b9
    initial_embed.title = 'Search results'
    initial_embed.description = 'Here are the results retrieved from Tankobon'
    for result in results:
        initial_embed.add_field(name=result['name'], value=f'`{config.COMMAND_PREFIX}manga ' + str(result['id']) + '`', inline=False)
    embeds.append(initial_embed)

    for i in range(loops):
        # Get the next page
        response = requests.get(f'{config.API_BASEURL}manga/?q={query}&offset={current_results}')
        if response.status_code == 200:
            json = response.json()
            r = json['manga']
            embed = Embed()
            embed.color = 0x52b9b9
            embed.title = 'Search results'
            embed.description = 'Here are the results retrieved from Tankobon'
            for result in r:
                embed.add_field(name=result['name'], value=f'`{config.COMMAND_PREFIX}manga ' + str(result['id']) + '`', inline=False)
            embeds.append(embed)
            current_results += 8

    return embeds

def get_recent_embed(results):
    embed = Embed()
    embed.color = 0x52b9b9
    embed.title = 'Recently updated Manga'
    for result in results:
        embed.add_field(name=result['name'], value=f'`{config.COMMAND_PREFIX}manga ' + str(result['id']) + '`', inline=False)

    return embed

def get_manga_embed(manga, volumes):
    embeds = []

    if volumes:
        for volume in volumes:
            embed = Embed()
            embed.color = 0x52b9b9
            embed.title = manga['name']
            embed.description = manga['description'].replace('<b>', '**').replace('</b>', '**').replace('<br>', '')
            embed.url = 'https://tankobon-manga.herokuapp.com/manga/' + str(manga['id'])

            if volume['poster']:
                embed.set_image(url=volume['poster'])
            elif manga['poster']:
                embed.set_image(url=manga['poster'])

            chapters = ''
            number = volume['number']

            name = ''
            if number == -1:
                name = 'Non-tankobon chapters'
            else:
                name = f'Volume {number}'

            if manga['romaji']:
                embed.add_field(name='Romaji', value=manga['romaji'], inline=True)

            if manga['volume_count']:
                embed.add_field(name='Volumes', value=manga['volume_count'], inline=True)

            if manga['status']:
                embed.add_field(name='Status', value=manga['status'], inline=True)

            if manga['start_date']:
                date = parser.parse(manga['start_date'])
                embed.add_field(name='Start Date', value=date.strftime("%B %d %Y"), inline=True)

            if manga['magazine']:
                embed.add_field(name='Serialization', value=manga['magazine'], inline=True)

            for chapter in volume['chapters']:
                if chapter.startswith('|'):
                    chapters += '*' + chapter.replace('|', '') + ' arc starts here*\n'
                else:
                    chapters += chapter + '\n'
            embed.add_field(name=name, value=chapters, inline=False)

            embeds.append(embed)
    else:
        embed = Embed()
        embed.color = 0x52b9b9
        embed.title = manga['name']
        embed.description = manga['description'].replace('<b>', '**').replace('</b>', '**').replace('<br>', '')
        embed.url = 'https://tankobon-manga.herokuapp.com/manga/' + str(manga['id'])

        if manga['poster']:
            embed.set_image(url=manga['poster'])

        if manga['romaji']:
            embed.add_field(name='Romaji', value=manga['romaji'], inline=True)

        if manga['volume_count']:
            embed.add_field(name='Volumes', value=manga['volume_count'], inline=True)

        if manga['status']:
            embed.add_field(name='Status', value=manga['status'], inline=True)

        if manga['start_date']:
            date = parser.parse(manga['start_date'])
            embed.add_field(name='Start Date', value=date.strftime("%B %d %Y"), inline=True)

        if manga['magazine']:
            embed.add_field(name='Serialization', value=manga['magazine'], inline=True)
        
        embeds.append(embed)

    return embeds

def get_help_embed():
    embed = Embed()
    embed.color = 0x52b9b9
    embed.title = 'Commands'
    embed.description = f'The prefix for these commands are {config.COMMAND_PREFIX}'
    embed.add_field(name='`search {query}`', value='Search for a manga. If only one result is returned, it will send the details for it.', inline=False)
    embed.add_field(name='`manga {id}`', value='Gets the details of a specific manga using the ID.', inline=False)
    embed.add_field(name='`recent`', value='Gets the 10 most recently updated manga.', inline=False)
    embed.add_field(name='`help`', value='Displays this message.', inline=False)
    return embed