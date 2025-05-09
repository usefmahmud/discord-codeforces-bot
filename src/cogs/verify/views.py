import discord
from discord import ui
from discord.ext import commands

from src.models.user import UserManager

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
            rating_roles = ['unrated', 'newbie', 'pupil', 'specialist', 'expert', 
                          'candidate master', 'master', 'international master',
                          'grandmaster', 'international grandmaster']
            
            for role in interaction.user.roles:
                if role.name.lower() in rating_roles:
                    await interaction.user.remove_roles(role)
            await interaction.response.edit_message(content='Account reset successfully.', view=None)
        
    @ui.button(label='Cancel', style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.orig_interaction.user.id:
            await interaction.response.send_message('You cannot interact with this button.', ephemeral = True)
            return
            
        await interaction.response.edit_message(content='Reset cancelled.', view = None)
