import discord
from discord.ext import commands

from src.config.settings import BOT_TOKEN, COMMAND_PREFIX

class MyBot(commands.Bot):
    
    def __init__(self):
        intents = discord.Intents.default()
        
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            intents=intents,
            help_command=None
        )
    
    async def setup_hook(self):
        '''Set up the bot by loading extensions and syncing commands.'''
        try:
            # Load cogs
            await self.load_extension('src.cogs.verify')
            print('Successfully loaded verify cog')
            
            # Sync commands
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(f'Error in setup_hook: {e}')
            raise
    
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
    
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Missing required argument: {error.param.name}')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Invalid argument provided')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('Command not found')
        else:
            await ctx.send('An error occurred while processing the command')

def main():
    try:
        bot = MyBot()
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f'Error running bot: {e}')
        raise