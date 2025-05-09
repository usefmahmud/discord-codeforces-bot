'''Verify cog for handling user verification with Codeforces.'''
from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands, ui

from src.models.user import UserManager
from src.api.codeforces import cf_client
from src.utils.discord_helpers import generate_verification_code, add_rank_role_to_user
from src.utils.embed_helpers import create_status_embed
from src.utils.error_helpers import format_error_message

from src.cogs.verify.views import ConfirmResetView

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
            
            cf_user = cf_client.get_user(handle)
            if not cf_user:
                await interaction.response.send_message('Invalid handle or Codeforces API error')
                return
            
            if user_data and not user_data['verified']:
                if cf_user.get('organization') == user_data['verification_code']:
                    if UserManager.update_user(interaction.user.id, verified = True):
                        await add_rank_role_to_user(
                            user_id = interaction.user.id,
                            role_name = cf_user['rank'],
                            guild = interaction.guild
                        )
                        UserManager.update_user(
                            interaction.user.id, 
                            rank = cf_user['rank'], 
                            rating = cf_user['rating']
                        )

                        await interaction.response.send_message('You are now verified! ✅')
                    else:
                        await interaction.response.send_message('Error updating verification status. Please try again.')
                else:
                    await interaction.response.send_message('Invalid verification code. Please try again.')
                return
            
            # New user verification
            if UserManager.is_handle_exists(handle):
                await interaction.response.send_message('Handle already exists. Please use a different handle.')
                return
          
            verification_code = generate_verification_code()
            if UserManager.add_user(
                user_id = interaction.user.id,
                name = interaction.user.name,
                handle = handle,
                verification_code = verification_code
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

    @app_commands.command(
        name='verify',
        description='Verify your account with your Codeforces handle'
    )
    async def verify(self, interaction: discord.Interaction, handle: str):
        user_data = UserManager.get(interaction.user.id)
        await self._handle_verification(interaction, handle, user_data)

    @app_commands.command(
        name='status',
        description='Check your verification status'
    )
    async def status(self, interaction: discord.Interaction):
        try:
            user_data = UserManager.get(interaction.user.id)
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


async def setup(bot: commands.Bot):
    await bot.add_cog(Verify(bot)) 