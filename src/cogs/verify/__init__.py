from src.cogs.verify.commands import Verify

async def setup(bot):
    await bot.add_cog(Verify(bot))
