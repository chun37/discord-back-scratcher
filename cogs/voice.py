from discord.ext import commands

from cogs.localcheck import exists_voice_client


class VoiceChat(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["vc"])
    async def voice_chat(self, ctx):
        pass

    @voice_chat.command(aliases=["join"])
    async def vc_join(self, ctx):
        voice = ctx.author.voice
        if voice is None:
            return
        await voice.channel.connect()

    @voice_chat.command(aliases=["leave"])
    @commands.check(exists_voice_client)
    async def vc_leave(self, ctx):
        voice_client = ctx.guild.voice_client
        await voice_client.disconnect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id != self.bot.user.id or before.channel is None:
            return
        voice_client = before.channel.guild.voice_client
        if voice_client is None:
            return
        await voice_client.disconnect()


def setup(bot):
    bot.add_cog(VoiceChat(bot))
