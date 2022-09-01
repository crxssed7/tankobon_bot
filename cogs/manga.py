import discord
import config
import requests
from discord.embeds import Embed
from discord.ext import commands
from cogs import utils
from disputils import BotEmbedPaginator, ControlEmojis

class Manga(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ce = ControlEmojis('⏮', '◀', '▶', '⏭', None)
    
    @commands.command()
    async def search(self, ctx, *text):
        query = f"{' '.join(text)}"
        if query:
            results = requests.get(f'{config.API_BASEURL}manga/?q={query}')
            if results.status_code == 200:
                json = results.json()
                total = json['total_results']
                if len(json['manga']) == 1:
                    # One manga, send that
                    manga = json['manga'][0]
                    _id = manga['id']
                    response = requests.get(f'{config.API_BASEURL}manga/{_id}/volumes/')
                    volumes = response.json()
                    msg = utils.get_manga_embed(manga, volumes)
                    paginator = BotEmbedPaginator(ctx, msg, control_emojis=self.ce)
                    await paginator.run()
                elif len(json['manga']) > 1:
                    manga = json['manga']
                    msg = utils.search_manga_embed(manga, total, query)
                    paginator = BotEmbedPaginator(ctx, msg, control_emojis=self.ce)
                    await paginator.run()
                else:
                    await ctx.send('No results found')
            else:
                await ctx.send(config.ERROR_MSG)
        else:
            await ctx.send('You must specify a query.')
    
    @commands.command()
    async def manga(self, ctx, text):
        try:
            _id = int(text)
            result = requests.get(f'{config.API_BASEURL}manga/{_id}')
            if result.status_code == 200:
                manga = result.json()
                v = requests.get(f'{config.API_BASEURL}manga/{_id}/volumes/')
                volumes = v.json()
                msg = utils.get_manga_embed(manga, volumes)
                paginator = BotEmbedPaginator(ctx, msg, control_emojis=self.ce)
                await paginator.run()
            elif result.status_code == 404:
                await ctx.send('Manga with that ID does not exist.')
        except ValueError:
            await ctx.send('You must provide a number.')
    
    @commands.command()
    async def recent(self, ctx):
        result = requests.get(f'{config.API_BASEURL}manga/?sort=last_updated&limit=10')
        if result.status_code == 200: 
            json = result.json()
            manga = json['manga']
            await ctx.send(embed=utils.get_recent_embed(manga))
        else:
            await ctx.send(config.ERROR_MSG)

    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=utils.get_help_embed())

def setup(bot):
    bot.add_cog(Manga(bot))