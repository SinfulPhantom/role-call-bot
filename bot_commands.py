import discord
from discord.ext import commands
from discord.utils import get

from config_manager import add_config_value


class BotCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="att_setup")
    async def att_setup(self, ctx: commands.Context, arg1="help", arg2=None):
        has_permission = permission_check(ctx.author.roles)
        commands_to_add = {
            "set_attendance_channel": "attendance_channel",
            "set_command_channel": "command_channel",
            "add_role": "allowed_roles",
        }
        if not has_permission:
            await ctx.send("You do not have the permission required to use this command!")
        elif str(ctx.channel) != "bot-commands":
            await ctx.send("You must be in the bot-commands channel to use this command!")
        else:
            if arg1 == "help":
                await ctx.send(embed=embed_commands())
            if arg1 in commands_to_add.keys():
                if arg1 == "set_attendance_channel_id" or arg1 == "set_command_channel":
                    if not get(ctx.guild.channels, id=arg2):
                        await ctx.send("Channel does not exist!")
                        return
                    result = add_config_value(commands_to_add.get(arg1), arg2)
                    await ctx.send(embed=embed_results(result))
                else:
                    print(get(ctx.guild.roles))
                    if arg2 not in get(ctx.guild.roles):
                        await ctx.send("Role does not exist!")
                        return
                    result = add_config_value(commands_to_add.get(arg1), arg2)
                    await ctx.send(embed=embed_results(result))

    @commands.command(name="attendance")
    async def attendance(self, ctx: commands.Context, arg1):
        channel = arg1
        voice_channel_id = discord.utils.get(ctx.guild.channels, name=channel).id
        voice_channel = self.bot.get_channel(voice_channel_id)
        att_channel = self.bot.get_channel(984140918368124951)
        role_call = []

        for member in voice_channel.members:
            role_call.append(member.name)

        member_per_line = '\n'.join(role_call)
        await att_channel.send(embed=embed_message(
            vc_members=member_per_line,
            channel=voice_channel)
        )
        await ctx.message.delete()


def permission_check(user_roles):
    for role in user_roles:
        if 978804043801571428 == role.id:
            return True
    return False


def embed_message(vc_members, channel):
    embed = discord.Embed(
        title=f"{channel}",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1248967471475740672/AeQ6udtQ_400x400.jpg")
    embed.add_field(name="Members", value='>>> {}'.format(vc_members))
    return embed


def embed_results(result):
    embed = discord.Embed(
        title=result,
        color=discord.Color.green()
    )
    return embed


def embed_commands():
    embed = discord.Embed(
        title="Attendance Setup Help",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1248967471475740672/AeQ6udtQ_400x400.jpg")
    att_commands = [
        "set_attendance_channel <id>",
        "set_command_channel <id>",
        "add_role <id>",
        "remove_role <id>"
    ]
    command_per_line = '\n'.join(att_commands)
    embed.add_field(name="Commands", value=">>> {}".format(command_per_line))
    return embed


def setup(bot: commands.Bot):
    bot.add_cog(BotCommands(bot))
