from discord.ext.commands import BotMissingPermissions, Cog


def snake_case_to_title_case(string):
    return string.replace("_", " ").title()


class CustomCog(Cog):
    async def cog_command_error(self, ctx, error):
        if isinstance(error, BotMissingPermissions):
            missing_perms_txt = (
                f"`{snake_case_to_title_case(permission)}`"
                for permission in error.missing_perms
            )
            await ctx.send(f"権限 {', '.join(missing_perms_txt)} を追加してください")
            return
        return await super().cog_command_error(ctx, error)
