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
                        player_list = data["players"]["list"]
                        players = "\n".join(player_list) if player_list else "None"
                        embed = discord.Embed(
                            title="Minecraft Server Status",
                            description=f"The server is online with {player_count} players.",
                            color=discord.Color.green()
                        )
                        embed.add_field(name="Players Online", value=players, inline=False)
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Minecraft Server Status",
                            description="The server is online, but no players are currently connected.",
                            color=discord.Color.green()
                        )
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Minecraft Server Status",
                        description="The server is offline or unreachable.",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=embed)
    except Exception:
        embed = discord.Embed(
            title="Minecraft Server Status",
            description="An error occurred while checking the server status.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)        



        
@bot.event
async def on_slash_command_error(ctx, ex):
    await ctx.send(str(ex))

bot.run(TOKEN)

