import discord
import string
import random
from datetime import datetime

def generate_verification_code(prefix: str = 'CF', length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f'{prefix}-{random_part}'

async def create_role(
    guild: discord.Guild,
    role_name: str,
    role_permissions: list[discord.Permissions],
    role_color: discord.Color,
    role_mentionable: bool
) -> discord.Role:
    role = await guild.create_role(
        name = role_name,
        permissions = role_permissions,
        color = role_color,
        mentionable = role_mentionable
    )
    
    return role

async def add_role_to_user(
    user: discord.Member,
    role: discord.Role
) -> None:
    await user.add_roles(role)

async def remove_role_from_user(
    user: discord.Member,
    role: discord.Role
) -> None:
    if role in user.roles:
        await user.remove_roles(role)
