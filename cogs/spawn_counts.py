from discord import File, Member
from discord.ext import commands
import discord
import requests
from easy_pil import Editor, Canvas, load_image_async, Font, load_image, Text
from discord.ext import commands, tasks

class spawn_counts(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.update_status.start()
        
    @tasks.loop(minutes=1)
    async def update_status(self):
        await self.bot.wait_until_ready()

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"a!help | {len(self.bot.guilds): ,} servers",
            )
        )

    @commands.hybrid_command(aliases=["sl"], description="View how many more spawns can be identified")
    async def spawnlimit(self, ctx):
        try:
            guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
            spawn_co = int(guild["spawn_count"])
        except:
            spawn_co = 1
            
        if spawn_co >= 750:
            percentage = 100
        else:
            x = spawn_co / 750
            percentage = int((x % 1) * 100 // 1)
        #file = make_card(ctx.guild, spawn_co, percentage, ctx.guild.icon.url)
        
        user_data = {  # Most likely coming from database or calculation
            "name": ctx.guild.name,  # The user's name
            "xp": spawn_co,
            "percentage": percentage,
        }

        background = Editor(Canvas((934, 282), "#8F9296"))
        
        profile_image = load_image(str(ctx.guild.icon.url))
        profile = Editor(profile_image).resize((190, 190)).circle_image()

        poppins = Font.poppins(size=30)

        background.rectangle((20, 20), 894, 242, "#2a2e35")
        background.paste(profile, (50, 50))
        background.ellipse((42, 42), width=206, height=206, outline="#43b581", stroke_width=10)
        background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
        background.bar(
            (260, 180),
            max_width=630,
            height=40,
            percentage=user_data["percentage"],
            fill="#00fa81",
            radius=20,
        )
        background.text((270, 120), user_data["name"], font=poppins, color="#FFFFFF")
        background.text(
            (870, 125),
            f"{user_data['xp']} / 750",
            font=poppins,
            color="#00fa81",
            align="right",
        )
        
        rank_level_texts = [
            Text("Used ", color="#00fa81", font=poppins),
            Text(f"{user_data['xp']}", color="#1EAAFF", font=poppins),
            Text("   Total ", color="#00fa81", font=poppins),
            Text(f"500", color="#1EAAFF", font=poppins),
        ]

        background.multicolor_text((850, 30), texts=rank_level_texts, align="right")
        file = File(fp=background.image_bytes, filename="card.png")
        await ctx.send(file=file)


async def setup(bot):
    print("Loaded Spawn Counts")
    await bot.add_cog(spawn_counts(bot))
