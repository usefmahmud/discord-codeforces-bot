'''Helper functions for the Discord Codeforces Verification Bot.'''
import string
import random
import logging
from typing import Optional
import discord
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_verification_code(prefix: str = 'CF', length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f'{prefix}-{random_part}'

def create_status_embed(user: discord.User, user_data: dict, is_info: bool = False) -> discord.Embed:
    embed = discord.Embed(
        title='Verification Status',
        color=discord.Color.green() if user_data['verified'] else discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    
    embed.set_author(
        name=user.name,
        icon_url=user.display_avatar.url if user.display_avatar else None
    )
    
    embed.add_field(
        name='Codeforces Handle',
        value=user_data['handle'],
        inline=True
    )
    
    embed.add_field(
        name='Status',
        value='✅ Verified' if user_data['verified'] else '⏳ Pending',
        inline=True
    )

    embed.add_field(
        name='Rating',
        value=f'{user_data["rating"]} ({user_data["rank"]})',
        inline=True
    )
    
    if not is_info:
        if not user_data['verified']:
            embed.add_field(
                name='Verification Code',
                value=f'`{user_data["verification_code"]}`',
                inline=False
            )
            embed.add_field(
                name='Instructions',
                value=(
                    '1. Go to your Codeforces profile settings\n'
                    '2. Change your organization to the verification code above\n'
                    '3. Run `/verify` command again'
                ),
                inline=False
            )

    embed.set_footer(text='Last updated')
    return embed

def format_error_message(error: Exception) -> str:
    error_type = type(error).__name__
    error_msg = str(error)
    logger.error(f'{error_type}: {error_msg}')
    
    if isinstance(error, discord.errors.Forbidden):
        return 'I don\'t have permission to perform this action'
    elif isinstance(error, discord.errors.HTTPException):
        return 'Discord API error occurred. Please try again later'
    else:
        return 'An unexpected error occurred. Please try again later' 