import discord
from discord.ext import commands
import json
import glob
from models import MusicQueue, MusicItem
from collections import defaultdict

def exists_voice_client(ctx):
    return bool(ctx.guild.voice_client)


class VoiceChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._queue_setup()

    def _queue_setup(self):
        self.queues = defaultdict(MusicQueue)
        queue_files = glob.glob("./data/*/queue.json")
        for file in queue_files:
            pass

    def _load_json(self, file_path):
        with open(file_path) as f:
            data = json.loads(f.read())
        return data

    async def _add_queue(self, ctx, item):
        pass

    async def _get_queue(self, guild_id):
        pass


    def _get_voice_client(self, guild_id):
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
    async def on_voice_state_update(self, member, before, after):
        if member.id != self.bot.user.id or before.channel is None:
            return
        voice_client = before.channel.guild.voice_client
        if voice_client is None:
            return
        await voice_client.disconnect()

    @voice_chat.command(aliases=["play"])
    @commands.check(exists_voice_client)
    async def vc_play(self, ctx):
        await self._add_queue(ctx, "./music/01 響鳴.m4a")
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        source = discord.FFmpegPCMAudio("./music/01 響鳴.m4a")
        voice_client.play(source)

    @voice_chat.command(aliases=["pause"])
    @commands.check(exists_voice_client)
    async def vc_pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing() is False:
            return
        voice_client.pause()

    @voice_chat.command(aliases=["resume"])
    @commands.check(exists_voice_client)
    async def vc_resume(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_paused() is False:
            return
        voice_client.resume()

    @voice_chat.command(aliases=["stop"])
    @commands.check(exists_voice_client)
    async def vc_stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing() is False:
            return
        voice_client.stop()

    @voice_chat.command(aliases=["queue"])
    async def vc_queue(self, ctx):
        print(self.queues[ctx.guild.id])
        pass



def setup(bot):
    bot.add_cog(VoiceChat(bot))
