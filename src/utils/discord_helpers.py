import discord
import string
import random
from datetime import datetime
from typing import Literal

rank_roles = [
    'unrated',
    'newbie',
    'pupil',
    'specialist',
    'expert',
    'candidate master',
    'master',
]

def generate_verification_code(prefix: str = 'CF', length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f'{prefix}-{random_part}'

async def add_rank_role_to_user(
    user_id: int,
    role_name: Literal[
        'unrated',
        'newbie',
        'pupil',
        'specialist',
        'expert',
        'candidate master',
        'master',
    ],
    guild: discord.Guild
) -> None:
    user = guild.get_member(user_id)
    if not user:
        return

    server_roles = user.guild.roles
    for role in server_roles:
        if role.name.lower() == role_name:
            await user.add_roles(role)

async def remove_rank_role_from_user(
    user_id: int,
    guild: discord.Guild
) -> None:
    user = guild.get_member(user_id)
    if not user:
        return

    for role in user.roles:
        if role.name.lower() in rank_roles:
            await user.remove_roles(role)
