'''Verify cog for handling user verification with Codeforces.'''
from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands, ui

from src.models.database import db
from src.api.codeforces import cf_client
from src.utils.helpers import generate_verification_code, create_status_embed, format_error_message

class Verify(commands.Cog):    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def _handle_verification(
        self,
        interaction: discord.Interaction,
        handle: str,
        user_data: Optional[dict]
    ) -> None:
        try:
            if user_data and user_data['verified']:
                await interaction.response.send_message('You are already verified')
                return
            
            cf_user = cf_client.get_user_info(handle)
            if not cf_user:
                await interaction.response.send_message('Invalid handle or Codeforces API error')
                return
            
            if user_data and not user_data['verified']:
                if cf_user.get('organization') == user_data['verification_code']:
                    if db.update_user_verification(interaction.user.id, True):
                        await self._add_user_role(interaction, cf_user)
                        await db.update_user_rank_and_rating(interaction.user.id, cf_user['rank'], cf_user['rating'])
                        await interaction.response.send_message('You are now verified! ✅')
                    else:
                        await interaction.response.send_message('Error updating verification status. Please try again.')
                else:
                    await interaction.response.send_message('Invalid verification code. Please try again.')
                return
            
            # New user verification
            verification_code = generate_verification_code()
            if db.add_user(
                interaction.user.id,
                interaction.user.name,
                handle,
                verification_code,
                rank = '',
                rating = 0
            ):
                await interaction.response.send_message(
                    f'To complete verification:\n'
                    f'1. Go to your Codeforces profile settings\n'
                    f'2. Change your organization to: `{verification_code}`\n'
                    f'3. Run this command again'
                )
            else:
                await interaction.response.send_message('Error creating verification. Please try again.')
        except Exception as e:
            await interaction.response.send_message(format_error_message(e))

    async def _add_user_role(self, interaction: discord.Interaction, user_data: dict) -> None:
        guild = interaction.guild
        role_name = user_data['rank']
        role_color = cf_client.get_user_rating_colour(user_data['rank'])
        role_permissions = discord.Permissions.none()
        role_mentionable = True

        role = await guild.create_role(
            name = role_name, 
            permissions = role_permissions, 
            color = role_color, 
            mentionable = role_mentionable
        )

        if not role.id:
            return
        
        await interaction.user.add_roles(role)

    @app_commands.command(
        name='verify',
        description='Verify your account with your Codeforces handle'
    )
    async def verify(self, interaction: discord.Interaction, handle: str):
        user_data = db.get_user(interaction.user.id)
        await self._handle_verification(interaction, handle, user_data)

    @app_commands.command(
        name='status',
        description='Check your verification status'
    )
    async def status(self, interaction: discord.Interaction):
        try:
            user_data = db.get_user(interaction.user.id)
            if not user_data:
                await interaction.response.send_message('You haven\'t started verification yet. Use `/verify` to begin.')
                return

            embed = create_status_embed(interaction.user, user_data)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(format_error_message(e))

    @app_commands.command(
        name='reset',
        description='Reset your account'
    )
    async def reset(self, interaction: discord.Interaction):
        confirm_view = ConfirmResetView(self.bot, timeout=60)
        await interaction.response.send_message(
            'Are you sure you want to reset account? \n This will remove your verification. \n', 
            view = confirm_view
        )
        
        confirm_view.orig_interaction = interaction

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
            
        if not db.reset_user(interaction.user.id):
            await interaction.response.edit_message(content='Error resetting account. Please try again.', view = None)
        else:
            role = interaction.guild.get_role(interaction.user.roles[-1].id)
            if role:
                await interaction.user.remove_roles(role)
            await interaction.response.edit_message(content='Account reset successfully.', view=None)
        
    @ui.button(label='Cancel', style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: ui.Button):
        if interaction.user.id != self.orig_interaction.user.id:
            await interaction.response.send_message('You cannot interact with this button.', ephemeral = True)
            return
            
        await interaction.response.edit_message(content='Reset cancelled.', view = None)

async def setup(bot: commands.Bot):
    await bot.add_cog(Verify(bot)) 