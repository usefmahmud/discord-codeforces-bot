import discord
from discord import ui
from discord.ext import commands

from src.models.user import UserManager
from src.utils.discord_helpers import remove_rank_role_from_user
class ConfirmResetView(ui.View):
    '''View for confirming or cancelling a reset.'''
    def __init__(self, bot: commands.Bot, timeout: int):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.orig_interaction = None
        
    @ui.button(label='Confirm Reset', style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.orig_interaction.user.id:
            await interaction.response.send_message('You cannot interact with this button.', ephemeral = True)
            return
            
        if not UserManager.reset_user(interaction.user.id):
            await interaction.response.edit_message(content='Error resetting account. Please try again.', view = None)
        else:
            await remove_rank_role_from_user(
                user_id = interaction.user.id,
                guild = interaction.guild
            )
            await interaction.response.edit_message(content='Account reset successfully.', view=None)
        
    @ui.button(label='Cancel', style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.orig_interaction.user.id:
            await interaction.response.send_message('You cannot interact with this button.', ephemeral = True)
            return
            
        await interaction.response.edit_message(content='Reset cancelled.', view = None)
