import discord
from discord import app_commands
from discord.ext import commands
from src.models.problem import ProblemManager
from src.data.constants import LITERAL_TAGS, LITERAL_RATING
from typing import Optional

class Problem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="problem", description="Get a random problem")
    async def problem(
        self, 
        interaction: discord.Interaction, 
        tag: Optional[LITERAL_TAGS] = None, 
        rating: Optional[LITERAL_RATING] = None
      ):
        print('tag', tag)
        problem = ProblemManager.get_random_problem(tag, rating )
        if problem:
            print('problem', problem)
            await interaction.response.send_message(f"Problem: {problem['name']}\nRating: {problem['rating']}\nTags: {', '.join(problem['tags'])}")
        else:
            await interaction.response.send_message("No problems found")

async def setup(bot: commands.Bot):
    await bot.add_cog(Problem(bot))