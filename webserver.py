from quart import Quart
from discord.ext import ipc


app = Quart(__name__)
ipc_client = ipc.Client(secret_key="192b9bdd21ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d53727823bcbf")


@app.route("/")
async def index():
    member_count = await ipc_client.request(
        "get_member_count", guild_id=12345678
    )  # get the member count of server with ID 12345678

    return str(member_count)  # display member count


if __name__ == "__main__":
    app.run()
