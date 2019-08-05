import json
import glob
from collections import defaultdict

import discord
from discord.ext import commands

from models import MusicQueue, MusicItem
from cogs.localcheck import exists_voice_client


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._queue_setup()

    def _load_json(self, file_path):
        with open(file_path) as f:
            data = json.loads(f.read())
        return data

    async def _add_queue(self, ctx, item):
        pass

    async def _get_queue(self, guild_id):
        pass

    def _queue_setup(self):
        self.queues = defaultdict(MusicQueue)
        queue_files = glob.glob("./data/*/queue.json")
        for file in queue_files:
            pass

    @commands.group(aliases=["music"])
    async def music(self, ctx):
        pass

    @music.command(aliases=["play"])
    @commands.check(exists_voice_client)
    async def vc_play(self, ctx):
        await self._add_queue(ctx, "./music/01 響鳴.m4a")
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        source = discord.FFmpegPCMAudio("./music/01 響鳴.m4a")
        voice_client.play(source)

    @music.command(aliases=["pause"])
    @commands.check(exists_voice_client)
    async def vc_pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing() is False:
            return
        voice_client.pause()

    @music.command(aliases=["resume"])
    @commands.check(exists_voice_client)
    async def vc_resume(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_paused() is False:
            return
        voice_client.resume()

    @music.command(aliases=["stop"])
    @commands.check(exists_voice_client)
    async def vc_stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing() is False:
            return
        voice_client.stop()

    @music.command(aliases=["queue"])
    async def vc_queue(self, ctx):
        print(self.queues[ctx.guild.id])
        pass


def setup(bot):
    bot.add_cog(Music(bot))
