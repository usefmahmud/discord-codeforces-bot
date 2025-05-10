import discord
from discord import app_commands
from discord.ext import commands
from src.models.problem import ProblemManager
from src.data.constants import LITERAL_TAGS, LITERAL_RATING
from typing import Optional
from src.utils.embed_helpers import create_problem_embed
from src.cogs.problem.views import ProblemFinishView

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
        
        problem = ProblemManager.get_random_problem(tag, rating )
        embed = create_problem_embed(problem)
        finish_view = ProblemFinishView(self.bot, problem)
        finish_view.orig_interaction = interaction
        await interaction.response.send_message(embed = embed, view = finish_view)


