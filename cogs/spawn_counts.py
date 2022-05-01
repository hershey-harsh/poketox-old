from discord import File, Member
from discord.ext import commands
from leveling.utils import get_user_data, get_rank
from easy_pil import Editor, Canvas, load_image_async, Font


class Level(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def rank(self, ctx):
        try:
            guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
            spawn_co = guild["spawn_count"]
        except:
            spawn_co = 0
            
        percentage = int(guild["spawn_count"]) / 750

        background = Editor("background.png")
        profile = await load_image_async(str(ctx.guild.icon_url))

        profile = Editor(profile).resize((150, 150)).circle_image()

        poppins = Font().poppins(size=40)
        poppins_small = Font().poppins(size=30)

        square = Canvas((500, 500), "#06FFBF")
        square = Editor(square)
        square.rotate(30, expand=True)

        background.paste(square.image, (600, -250))
        background.paste(profile.image, (30, 30))

        background.rectangle((30, 220), width=650, height=40, fill="white", radius=20)
        background.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=percentage,
            fill="#FF56B2",
            radius=20,
        )
        background.text((200, 40), str(ctx.guild), font=poppins, color="white")

        background.rectangle((200, 100), width=350, height=2, fill="#17F3F6")
        background.text(
            (200, 130),
            f"Limit : 750"
            + f" Used : {spawn_co} / {750}",
            font=poppins_small,
            color="white",
        )

        file = File(fp=background.image_bytes, filename="card.png")
        await ctx.send(file=file)


def setup(bot):
    bot.add_cog(Level(bot))
