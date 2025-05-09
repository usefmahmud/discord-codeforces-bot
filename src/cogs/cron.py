import os
import discord
import time
from discord import app_commands
from discord.ext import commands, tasks

from src.models.user import UserManager
from src.api.codeforces import cf_client
from src.utils.discord_helpers import remove_rank_role_from_user, add_rank_role_to_user

class Cron(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.announcement_channel_id = int(os.getenv('ANNOUNCEMENT_CHANNEL_ID'))
        self.guild = int(os.getenv('SERVER_ID'))


    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(self.guild)
        self.announcement_channel = self.guild.get_channel(self.announcement_channel_id)
        self.update_user_ratings.start()
    
    @tasks.loop(hours = 24)
    async def update_user_ratings(self):
        for user in UserManager.get_all():
            user_data = UserManager.get(user['user_id'])
            if not user_data:
                continue
            
            new_user = cf_client.get_user(user['handle'])
            if not new_user:
                print(f'Error getting user {user["handle"]} from Codeforces')

            if new_user['rating'] == user_data['rating']:
                continue

            UserManager.update_user(
                user['user_id'],
                rating = new_user['rating'],
                rank = new_user['rank'],
            )

            if new_user['rank'] != user_data['rank']:
                await remove_rank_role_from_user(
                    user_id = user['user_id'],
                    guild = self.guild
                )

                await add_rank_role_to_user(
                    user_id = user['user_id'],
                    role_name = new_user['rank'],
                    guild = self.guild
                )
                
                

            time.sleep(1)
        
        if self.announcement_channel:
            await self.announcement_channel.send('All user ratings and ranks has been updated!')
        else:
            print('Channel not found')

    

async def setup(bot: commands.Bot):
    await bot.add_cog(Cron(bot))