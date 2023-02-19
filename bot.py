from discord.ext import commands
from discord import Invite, Member

import logging

logger = logging.getLogger("info")
error_logger = logging.getLogger("error")


class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        logger.info(f"{self.user.name} has connected to the discord!")

    @staticmethod
    async def on_invite_create(invite: Invite):
        logger.info(f"{invite.inviter} has created an invite")
        if invite.inviter.id == 213690694236241920:
            # Prevent auto-delete of invite created by Andrew Brown
            return
        if isinstance(invite.inviter, Member) and invite.inviter.guild_permissions.manage_channels:
            # Prevent auto delete of invite created by users with manage channel permission
            return
        await invite.delete(reason="auto delete")
