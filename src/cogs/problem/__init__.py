from src.cogs.problem.commands import Problem

async def setup(bot):
    await bot.add_cog(Problem(bot))