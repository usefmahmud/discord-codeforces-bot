import discord
from discord import ui
import math
from src.models.problem import ProblemManager

class PaginatorView(ui.View):
    def __init__(self, problems, per_page = 5):
        super().__init__()
        self.problems = problems
        self.per_page = per_page
        self.total_pages = math.ceil(len(self.problems) / self.per_page)
        self.page = 0
        
        self.embed = discord.Embed(title = f'Solved Problems ({len(self.problems)}) / {ProblemManager.get_total_problems_count()}')
        self.update_embed()

    def update_embed(self):
        start = self.page * self.per_page
        end = start + self.per_page

        self.embed.clear_fields()
        for i, problem in enumerate(self.problems[start : end], start = start + 1):
            self.embed.add_field(
                name = f'Problem {i}', 
                value = f'''
                  [{problem["index"]}. {problem["name"]}](https://codeforces.com/problemset/problem/{problem["contest_id"]}/{problem["index"]})
                  rating: {problem["rating"]}
                ''', 
                inline = False
              )
        self.embed.set_footer(text = f'Page {self.page + 1} of {self.total_pages}')

    async def update_message(self, interaction: discord.Interaction):
        self.update_embed()
        await interaction.response.edit_message(embed = self.embed, view = self)

    @ui.button(label = '<', style = discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page -= 1
            await self.update_message(interaction)
        else:
            await interaction.response.send_message('You are on the first page', ephemeral = True)

    @ui.button(label = '>', style = discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if (self.page + 1) * self.per_page < len(self.problems):
            self.page += 1
            await self.update_message(interaction)
        else:
            await interaction.response.send_message('You are on the last page', ephemeral = True)
