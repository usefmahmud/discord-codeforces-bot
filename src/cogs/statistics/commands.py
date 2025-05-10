import discord
from discord import app_commands
from discord.ext import commands
from src.models.problem import ProblemManager
from src.cogs.statistics.views import PaginatorView
from src.data.constants import LITERAL_STATISTICS_TYPE

class Statistics(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = 'statistics', description = 'Show your statistics')  
    async def statistics(self, interaction: discord.Interaction, type: LITERAL_STATISTICS_TYPE):
        if type == 'solved problems':
            problems = ProblemManager.get_solved_problems(interaction.user.id)
            if not problems:
                await interaction.response.send_message('You have not solved any problems yet')
                return
            
            paginator = PaginatorView(problems)
            await interaction.response.send_message(embed = paginator.embed, view = paginator)
    

