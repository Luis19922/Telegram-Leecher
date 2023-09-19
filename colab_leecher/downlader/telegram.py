
import logging
from datetime import datetime
from os import path as ospath
from colab_leecher import colab_bot
from colab_leecher.utility.handler import cancelTask
from colab_leecher.utility.variables import Transfer, Paths
from colab_leecher.utility.helper import speedETA, getTime, sizeUnit, status_bar

async def media_Identifier(link):
    parts = link.split("/")
    message_id = parts[-1]
    msg_chat_id = "-100" + parts[4]
    message_id, msg_chat_id = int(message_id), int(msg_chat_id)
    message = await bot.get_messages(msg_chat_id, message_id)
try:
message = await colab_bot.get_messages(msg_chat_id, message_id)
    except Exception as e:
        logging.error(f"Error getting messages {e}")
        
    media = (
        message.document  # type: ignore
        or message.photo  # type: ignore
        or message.video  # type: ignore
        or message.audio  # type: ignore
        or message.voice  # type: ignore
        or message.video_note  # type: ignore
        or message.sticker  # type: ignore
        or message.animation  # type: ignore
        or None
    )
    if media is None:
        raise Exception("Couldn't Download Telegram Message")
    return media, message


async def download_progress(current, total):
    speed_string, eta, percentage = speed_eta(start_time, current, total)

    await status_bar(
        down_msg=down_msg,
        speed=speed_string,
        percentage=percentage,
        eta=convert_seconds(eta),
        done=size_measure(sum(down_bytes) + current),
        left=size_measure(folder_info[0]),
        engine="Pyrogram 💥",
    )


async def TelegramDownload(link, num):
    global start_time, down_msg, TRANSFER_INFO
    media, message = await media_Identifier(link)
    if media is not None:
        name = media.file_name if hasattr(media, "file_name") else "None"  # type: ignore
    else:
        raise Exception("Couldn't Download Telegram Message")

    down_msg = f"<b>📥 DOWNLOADING FROM » </b><i>🔗Link {str(num).zfill(2)}</i>\n\n<code>{name}</code>\n"
    start_time = datetime.datetime.now()
    file_path = ospath.join(d_fol_path, name)
    await message.download(  # type: ignore
        progress=download_progress, in_memory=False, file_name=file_path
    )
    down_bytes.append(media.file_size)
