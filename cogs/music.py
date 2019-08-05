import queue
import functools
from collections import defaultdict

import discord
import aiosqlite
from discord.ext import commands

from models import LocalMusicItem
from cogs.localcheck import exists_voice_client


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = defaultdict(lambda: queue.Queue())
        self.queues_list = defaultdict(list)
        self.nowplaying = defaultdict(lambda: LocalMusicItem())

    def _add_queue(self, ctx, item):
        self.queues[ctx.guild.id].put(item)
        self.queues_list[ctx.guild.id].append(item)
        return

    def _list_queue(self, ctx):
        return self.queues_list[ctx.guild.id]

    def _get_queue(self, ctx):
        if len(self.queues_list[ctx.guild.id]) == 0:
            return
        item = self.queues[ctx.guild.id].get_nowait()
        self.queues_list[ctx.guild.id].remove(item)
        return item

    async def _fetch_async(self, fetch_type, query):
        async with aiosqlite.connect('./music/localdata.db') as con:
            async with con.execute(query) as cur:
                if fetch_type == "one":
                    row = await cur.fetchone()
                elif fetch_type == "all":
                    row = await cur.fetchall()
        return row

    @commands.group()
    async def music(self, ctx):
        pass

    @music.command(aliases=["play"])
    @commands.check(exists_voice_client)
    async def music_play(self, ctx, id_or_url):
        query = f"select * from local_music where id == {id_or_url}"
        _, title, artist, path = await self._fetch_async("one", query)
        item = LocalMusicItem(
            title=title,
            artist=artist,
            path=path,
            added=ctx.author)
        self._add_queue(ctx, item)
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            return
        self._cmd_play(ctx)

    def _play_after(self, *args):
        self._cmd_play(args[0])

    def _cmd_play(self, ctx):
        voice_client = ctx.guild.voice_client
        try:
            item = self._get_queue(ctx)
        except Exception as e:
            print(e)
            return
        source = discord.FFmpegPCMAudio(item.path)
        voice_client.play(
            source, after=functools.partial(self._play_after, ctx))

    @music.command(aliases=["pause"])
    @commands.check(exists_voice_client)
    async def music_pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing() is False:
            return
        voice_client.pause()

    @music.command(aliases=["resume"])
    @commands.check(exists_voice_client)
    async def music_resume(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_paused() is False:
            return
        voice_client.resume()

    @music.command(aliases=["stop"])
    @commands.check(exists_voice_client)
    async def music_stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing() is False:
            return
        voice_client.stop()

    @music.command(aliases=["queue"])
    async def music_queue(self, ctx):
        print(self.queues[ctx.guild.id])
        pass


def setup(bot):
    bot.add_cog(Music(bot))
