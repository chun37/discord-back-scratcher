from discord import Message, RawReactionActionEvent, TextChannel
from discord.ext.commands import Bot, command

from custom import CustomCog


class DeleteMessage(CustomCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @CustomCog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent) -> None:
        channel: TextChannel = await self.bot.fetch_channel(payload.channel_id)
        message: Message = await channel.fetch_message(payload.message_id)
        if message.author != self.bot.user:
            return
        if str(payload.emoji) != "\N{WASTEBASKET}\N{VARIATION SELECTOR-16}":
            return
        await message.delete()


def setup(bot: Bot) -> None:
    bot.add_cog(DeleteMessage(bot))
