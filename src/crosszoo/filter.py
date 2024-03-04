import asyncio
import logging
from collections import Counter
from datetime import datetime, timedelta, timezone
from logging import Logger
from typing import Self

from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_helper import ApiTelegramException
from telebot.types import ChatPermissions, Message, User

from crosszoo.settings import Settings

__all__ = ("Filter",)


class Filter:
    def __init__(self: Self) -> None:
        self.__logger: Logger = logging.getLogger(name="crosszoo.filter")
        self.__settings: Settings = Settings()  # type: ignore[call-arg]

        # This will count warnings.
        self.__counts: Counter = Counter()

        # Aliases via comma.
        self.__bot_aliases_to_allow: set[str] = set(self.__settings.BOT_ALIASES_TO_ALLOW.lower().split(","))
        self.__logger.info("Initializing filter, allow bots: %s", self.__bot_aliases_to_allow)

        # Initialize bot.
        self.__bot: AsyncTeleBot = AsyncTeleBot(self.__settings.BOT_TOKEN)

        # Setup handler.
        self.__bot.message_handler(
            # All content types.
            content_types=[
                "audio",
                "photo",
                "voice",
                "video",
                "document",
                "text",
                "location",
                "contact",
                "sticker",
                "gif",
                "animation",
            ]
        )(self.__handler)

        self.__logger.info("Filter is initialized.")

    async def start(self: Self) -> None:
        self.__logger.info("Filter started.")
        await self.__bot.infinity_polling()

    async def __handler(self: Self, message: Message) -> None:
        # Trigger only if via_bot is not None, or bot is not filtered.
        if message.via_bot is None or message.via_bot.username.lower() in self.__bot_aliases_to_allow:
            return

        try:
            await self.__bot.delete_message(message.chat.id, message.id)

        except Exception as exception:
            self.__logger.exception("Cannot delete message: %s", exception)

        else:
            self.__logger.info(
                "Message deleted from @%s and bot @%s", message.from_user.username, message.via_bot.username
            )

        if not self.__settings.MUTE:
            return

        try:
            await self.__mute_for(message.chat.id, message.from_user, period=timedelta(hours=1))

        except Exception as exception:
            self.__logger.exception("Cannot mute user: %s", exception)

    async def __mute_for(self: Self, chat_id: int | str, user: User, period: timedelta) -> None:
        end_date: datetime = datetime.now(tz=timezone.utc) + period

        try:
            # Mute.
            await self.__bot.restrict_chat_member(
                chat_id,
                user.id,
                end_date,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_audios=False,
                    can_send_documents=False,
                    can_send_photos=False,
                    can_send_videos=False,
                    can_send_video_notes=False,
                    can_send_voice_notes=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                ),
            )

        except ApiTelegramException as exception:
            if "user is an administrator of the chat" in exception.description:
                self.__counts[user.id] += 1

                if self.__counts[user.id] == self.__settings.WARNINGS:
                    await self.__bot.send_message(chat_id, text=f"Fuck it, @smthngslv ban @{user.username}, pls.")

                else:
                    await self.__bot.send_message(
                        chat_id, text=f"A few more times, and you gonna regret it, @{user.username}."
                    )

            return

        else:
            self.__logger.info("User @%s muted.", user.username)

        # Notification.
        await self.__bot.send_message(
            chat_id,
            text=f"Congratulations, @{user.username}! You've unlocked our exclusive 'Silent Reflection Hour' for "
            f"demonstrating unmatched enthusiasm in the art of spamming. Enjoy this peaceful moment to "
            f"contemplate the vast emptiness of a chat without your contributions. We'll see you on the other "
            f"side in 1 hour, refreshed and hopefully a tad less zealous. 🕒✨",
        )


async def main() -> None:
    await Filter().start()


if __name__ == "__main__":
    asyncio.run(main())
