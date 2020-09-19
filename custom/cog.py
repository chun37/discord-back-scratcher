import traceback

import discord
from discord.ext.commands import BotMissingPermissions, Cog

from utils import permissions_to_error_text


class CustomCog(Cog):
    async def cog_command_error(self, ctx, error):
        if isinstance(error, BotMissingPermissions):
            await ctx.send(permissions_to_error_text(error.missing_perms))
        else:
            traceback.print_exc()

    def on_message_bot_has_permissions(self, guild, channel, bot_user, **perms):
        invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
        if invalid:
            raise TypeError("Invalid permission(s): %s" % (", ".join(invalid)))

        me = guild.me if guild is not None else bot_user
        permissions = channel.permissions_for(me)

        missing = [
            perm for perm, value in perms.items() if getattr(permissions, perm) != value
        ]

        if not missing:
            return True

        raise BotMissingPermissions(missing)
