import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import aiohttp








@slash.slash(
    name="server_status",
    description="Check the status of a Minecraft server",
    options=[
        {
            "name": "server_ip",
            "description": "The IP address of the Minecraft server",
            "type": 3,  # String type
            "required": True
        }
    ]
)
async def server_status(ctx: SlashContext, server_ip: str):
    url = f"https://api.mcsrvstat.us/2/{server_ip}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if response.status == 200:
                    if data.get("online"):
                        player_count = data["players"]["online"]
                        players = "\n".join(data["players"]["list"])
                        await ctx.send(f"The server is online with {player_count} players: {players}")
                    else:
                        await ctx.send("The server is online, but no players are currently connected.")
                else:
                    await ctx.send("The server is offline or unreachable.")
    except Exception:
        await ctx.send("An error occurred while checking the server status.")


        
        
        
        
        
@bot.event
async def on_slash_command_error(ctx, ex):
    await ctx.send(str(ex))

bot.run(TOKEN)

