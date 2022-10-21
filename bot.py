from __future__ import print_function
from apiclient import discovery
from dotenv import load_dotenv

import discord
import httplib2
import os


load_dotenv()
GOOGLE_SHEETS_API_KEY = os.getenv('GOOGLE_SHEETS_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')


def main():

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('<NHR> Gemcutter Bot is online.')

    @client.event
    async def on_message(message):
        if message.content.lower().startswith('!gemcutter'):
            message_as_list = message.content.split(' ' , 1)

            if len(message_as_list) > 1:
                gem_name = message_as_list[1]
                result = search_spreadsheet(gem_name)
                await message.reply(result)
            else:
                await message.reply(
                    'Invalid command: missing gem name\nExample usage: !gemcutter Bright Scarlet Ruby')

    client.run(BOT_TOKEN)


def search_spreadsheet(gem_name):

    print(f'Searching which guildies can cut \'{gem_name}\'...')

    discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = discovery.build(
        'sheets',
        'v4',
        http=httplib2.Http(),
        discoveryServiceUrl=discovery_url,
        developerKey=GOOGLE_SHEETS_API_KEY)

    results_by_type = {
        'Red': [],
        'Yellow': [],
        'Blue': [],
        'Orange': [],
        'Green': [],
        'Purple': [],
        'Meta': [],
        'Dragon\'s Eye': []
    }

    for type in results_by_type.keys():
        range_name = f'{type}!A:B'
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        results_by_type[type] = result.get('values', [])

    gem_name_found = False

    for type in results_by_type:
        for row in results_by_type[type]:
            if row and row[0].lower() == gem_name.lower():
                if len(row) > 1:
                    result = f'{row[1]} can cut \'{row[0]}\'.'
                    return result
                else:
                    gem_name_found = True

    if gem_name_found:
        return f'Nobody can cut \'{gem_name}\' yet.'
    else:
        return f'\'{gem_name}\' is not a valid gem name.'


if __name__ == '__main__':
    main()
