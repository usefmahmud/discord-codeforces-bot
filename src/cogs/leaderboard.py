import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal
from src.models.database import db
from src.api.codeforces import cf_client

class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='leaderboard', description = 'Show the leaderboard')
    async def leaderboard(self, interaction: discord.Interaction, scope: Literal['codeforces', 'server']):
        leaderboard_list = []
        if scope == 'codeforces':
            leaderboard_list = db.get_leaderboard_by_rating()
        elif scope == 'server':
            await interaction.response.send_message('Server leaderboard is not available yet')
            return

        if len(leaderboard_list) == 0:
            await interaction.response.send_message('No data found')
            return
        
        description = f'**Top {len(leaderboard_list)} Players**\n'

        for user in leaderboard_list:
            description += f'''
              {cf_client.get_user_rating_icon(user['rank'])} **{user['handle']}**: {user['name']}
              Rating: {user['rank']} - {user['rating']} \n'''
        
        embed = discord.Embed(
            title = '🏆 Leaderboard', 
            description = description
          )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard(bot))

