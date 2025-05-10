import discord
from discord import ui
from discord.ext import commands

from src.models.user import UserManager

from src.api.codeforces import cf_client
class ProblemFinishView(ui.View):
    def __init__(self, bot: commands.Bot, problem: dict):
        super().__init__()
        self.bot = bot
        self.problem = problem
        self.orig_interaction = None

    @ui.button(label = 'Finish', style = discord.ButtonStyle.success)
    async def finish(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.orig_interaction.user.id:
            await interaction.response.send_message('You cannot interact with this button.', ephemeral = True)
            return
        
        if not UserManager.get(interaction.user.id):
            await interaction.response.send_message('You have not verified your handle yet. Please verify your handle using the `/verify` command.', ephemeral = True)
            return
        
        user = UserManager.get(interaction.user.id)
        if cf_client.check_problem_solved(user['handle'], self.problem['contest_id'], self.problem['index']):
            await interaction.response.send_message(f'You have succesfully solved the problem')
            button.disabled = True
            return

        await interaction.response.send_message(f'You have not solved the problem yet')

