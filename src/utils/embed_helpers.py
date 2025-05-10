import discord
from datetime import datetime
from typing import Dict

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

def create_leaderboard_embed(leaderboard_list: list[dict], rating_icons: dict) -> discord.Embed:
    description = f'**Top {len(leaderboard_list)} Players**\n'

    for user in leaderboard_list:
        description += f'''
          {rating_icons[user['rank']]} **{user['handle']}**: {user['name']}
          Rating: {user['rank']} - {user['rating']}
          Points: {user['points']}\n'''
    
    embed = discord.Embed(
        title = '🏆 Leaderboard', 
        description = description
      )
    
    return embed

def create_problem_embed(problem: dict) -> discord.Embed:
    if not problem:
        embed = discord.Embed(
            title = 'No problem found',
            color = discord.Color.red()
        )
        return embed
    
    embed = discord.Embed(
        title = problem['name'],
        description = f'**Rating:** {problem["rating"]}\n**Tags:** {", ".join(problem["tags"])}',
        url = f'https://codeforces.com/problemset/problem/{problem["contest_id"]}/{problem["index"]}',
        color = discord.Color.blue()
    )
    
    embed.set_author(
        name = 'Codeforces',
    )

    return embed

