import discord
from discord import app_commands
from discord.ext import commands
from src.models.user import UserManager
from src.utils.embed_helpers import create_status_embed


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name='info',
        description='Get information about the bot'
    )
    async def info(self, interaction: discord.Interaction, user: discord.Member):
        user_data = UserManager.get(user.id)
        if not user_data:
            await interaction.response.send_message('User not registered yet in the database')
            return
        embed = create_status_embed(user, user_data, is_info = True)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))