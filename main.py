import discord
from discord import app_commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()
token = getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True


client = Client()
tree = app_commands.CommandTree(client)


@tree.command(
    name="roll_call",
    description="This command snapshots the members of a specific VC.",
)
async def self(interaction: discord.Interaction, channel_id: str):
    voice_channel = client.get_channel(int(channel_id))
    roll_call = get_vc_members(voice_channel)
    await interaction.response.send_message(embed=embed_message(
        vc_members=roll_call,
        channel=voice_channel)
    )


def get_vc_members(voice_channel):
    member_list = []
    for member in voice_channel.members:
        member_list.append(member.name)
    if len(member_list) <= 0:
        return "Channel is empty"
    member_per_line = '\n'.join(member_list)
    return member_per_line


def embed_message(vc_members, channel):
    embed = discord.Embed(
        title=f"{channel}",
        color=discord.Color.green()
    )
    embed.add_field(name="Members", value='>>> {}'.format(vc_members))
    return embed


client.run(token)
