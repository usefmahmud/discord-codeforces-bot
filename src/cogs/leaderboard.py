import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal
from src.models.user import UserManager
from src.api.codeforces import cf_client
from src.utils.embed_helpers import create_leaderboard_embed

class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='leaderboard', description = 'Show the leaderboard')
    async def leaderboard(self, interaction: discord.Interaction, scope: Literal['codeforces', 'server']):
        leaderboard_list = []
        if scope == 'codeforces':
            leaderboard_list = UserManager.get_by_rating()
        elif scope == 'server':
            leaderboard_list = UserManager.get_by_points()

        if len(leaderboard_list) == 0:
            await interaction.response.send_message('No data found')
            return
        
        leaderboard_embed = create_leaderboard_embed(leaderboard_list, cf_client.rating_icons)  

        await interaction.response.send_message(embed  = leaderboard_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard(bot))

