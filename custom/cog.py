import traceback
from typing import Any, NoReturn, Optional

import discord
from discord import ClientUser, Guild, TextChannel
from discord.ext.commands import BotMissingPermissions, Cog, Context

from utils import permissions_to_error_text


class CustomCog(Cog):
    async def cog_command_error(self, ctx: Context, error: Exception) -> None:
        if isinstance(error, BotMissingPermissions):
            await ctx.send(permissions_to_error_text(error.missing_perms))
        else:
            traceback.print_exc()

    @staticmethod
    def on_message_bot_has_permissions(
        guild: Guild, channel: TextChannel, bot_user: ClientUser, **perms: Any
    ) -> Optional[NoReturn]:
        invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
        if invalid:
            raise TypeError("Invalid permission(s): %s" % (", ".join(invalid)))

        user = guild.me if guild is not None else bot_user
        permissions = channel.permissions_for(user)

        missing = [
            perm for perm, value in perms.items() if getattr(permissions, perm) != value
        ]

        if not missing:
            return None

        raise BotMissingPermissions(missing)
