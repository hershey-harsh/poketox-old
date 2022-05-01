from discord import File, Member
from discord.ext import commands
import requests
from easy_pil import Editor, Canvas, load_image_async, Font

class spawn_counts(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(alias=["sl"])
    async def spawnlimit(self, ctx):
        try:
            guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
            spawn_co = int(guild["spawn_count"])
        except:
            spawn_co = 1
            
        x = spawn_co / 750
        percentage = int((x % 1) * 100 // 1)
        file = make_card(ctx.guild, spawn_co, percentage, ctx.guild.icon.url)
        
        user_data = {  # Most likely coming from database or calculation
            "name": ctx.guild.name,  # The user's name
            "xp": spawn_co,
            "percentage": percentage,
        }

        background = Editor(Canvas((934, 282), "#23272a"))

        response = requests.get(str(ctx.guild.icon.url))
        file = open("pfp.png", "wb")
        file.write(response.content)
        file.close()
        profile = Editor("pfp.png").resize((190, 190)).circle_image()

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
        background.text((270, 120), user_data["name"], font=poppins, color="#00fa81")
        background.text(
            (870, 125),
            f"{user_data['xp']} / 750",
            font=poppins,
            color="#00fa81",
            align="right",
        )

        #background.multicolor_text((850, 30), texts=rank_level_texts, align="right")
        file = File(fp=background.image_bytes, filename="card.png")
        await ctx.send(file=file)


async def setup(bot):
    print("Loaded Spawn Counts")
    await bot.add_cog(spawn_counts(bot))
