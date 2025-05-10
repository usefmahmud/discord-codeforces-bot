from src.cogs.statistics.commands import Statistics

async def setup(bot):
    await bot.add_cog(Statistics(bot))
