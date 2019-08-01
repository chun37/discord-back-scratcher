import discord
from discord.ext import commands


def exists_voice_client(ctx):
    return bool(ctx.guild.voice_client)


class VoiceChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_voice_client(self, guild_id):
        return self.bot.get_guild(guild_id).voice_client

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
    @commands.check(exists_voice_client)
    async def on_voice_state_update(self, member, before, after):
        if member.id != self.bot.user.id or before.channel is None:
            return
        voice_client = before.channel.guild.voice_client
        await voice_client.disconnect()

    @voice_chat.command(aliases=["play"])
    @commands.check(exists_voice_client)
    async def vc_play(self, ctx):
        voice_client = ctx.guild.voice_client
        source = discord.FFmpegPCMAudio("./music/01 響鳴.m4a")
        voice_client.play(source)


def setup(bot):
    bot.add_cog(VoiceChat(bot))
