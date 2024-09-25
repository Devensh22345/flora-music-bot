import asyncio

from pyrogram.enums import ChatType

import config
from WinxMusic import app
from WinxMusic.core.call import Winx
from WinxMusic.utils.database import (
    get_assistant,
    get_client,
    is_active_chat,
    is_autoend,
    set_loop,
)

from .seeker import autoend


async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        while not await asyncio.sleep(config.AUTO_LEAVE_ASSISTANT_TIME):
            from WinxMusic.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                left = 0
                try:
                    async for i in client.get_dialogs():
                        chat_type = i.chat.type
                        if chat_type in [
                            ChatType.SUPERGROUP,
                            ChatType.GROUP,
                            ChatType.CHANNEL,
                        ]:
                            chat_id = i.chat.id
                            if chat_id not in [config.LOG_GROUP_ID]:
                                if left == 20:
                                    continue
                                if not await is_active_chat(chat_id):
                                    try:
                                        await client.leave_chat(chat_id)
                                        left += 1
                                    except:
                                        continue
                except:
                    pass


async def auto_end():
    while not await asyncio.sleep(30):
        if not await is_autoend():
            continue
        for chat_id in autoend:
            count = autoend.get(chat_id)
            if not count or count == 0:
                try:
                    await Winx.stop_stream(chat_id)
                    await set_loop(chat_id, 0)
                    continue
                except:
                    continue
            if not await is_active_chat(chat_id):
                continue
            userbot = await get_assistant(chat_id)
            members = []
            async for member in userbot.get_call_members(chat_id):
                if member is None:
                    try:
                        await Winx.stop_stream(chat_id)
                        await set_loop(chat_id, 0)
                        continue
                    except:
                        continue
                members.append(member)

            if len(members) in [0, 1]:
                try:
                    await Winx.stop_stream(chat_id)
                    await set_loop(chat_id, 0)
                except:
                    continue
                try:
                    await app.send_message(
                        chat_id,
                        "Bot saiu do chat de voz devido à inatividade para evitar sobrecarga nos servidores. Ninguém estava ouvindo o bot no chat de voz.",
                    )
                except:
                    continue


asyncio.create_task(auto_leave())
asyncio.create_task(auto_end())
