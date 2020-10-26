from telethon import events, custom, Button
from telethon.tl.types import (
    Channel,
    Chat,
    User
)

import emoji
from googletrans import Translator
from userbot.utils import friday_on_cmd, edit_or_reply, sudo_cmd
from telethon.utils import get_display_name
from userbot.utils import friday_on_cmd, sudo_cmd
from userbot.uniborgConfig import Config
from telethon import events
from datetime import datetime
from userbot.utils import friday_on_cmd, edit_or_reply, sudo_cmd
import time
from userbot import Lastupdate, bot
import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.tl.types import ChannelParticipantsAdmins

from asyncio import sleep
from os import remove

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import MessageTooLongError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.utils import friday_on_cmd, errors_handler, register, sudo_cmd

# =================== CONSTANT ===================
PP_TOO_SMOL = "`Immagine troppo piccola bro`"
PP_ERROR = "`Purtroppo ho sbagliato a processare l'immagine`"
NO_ADMIN = "`Coglione non sono admin!`"
NO_PERM = (
    "`Non ho abbastanza permessi! :(`"
)
NO_SQL = "`Running on Non-SQL mode!`"

CHAT_PP_CHANGED = "`Ho cambiato la foto della chat`"
CHAT_PP_ERROR = (
    "`Non riesco a cambiare la foto,`"
    "`forse non sono admin,`"
    "`o non ho abbastanza permessi.`"
)
INVALID_MEDIA = "`Estensione del file sbagliata`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


@tgbot.on(events.NewMessage(pattern="^/bun(?: |$)(.*)"))
async def ban(event):
    noob = event.sender_id
    userids = []
    async for user in tgbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        userids.append(user.id)
    if noob not in userids:
        await event.reply("Non sei admin!")
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await event.reply("Non sono admin 🥺.")
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await event.reply("Non ho i permessi 🤭.")
        return
    # Helps ban group join spammers more easily
    try:
        reply = await event.get_reply_message()
        if reply:
             pass
    except BadRequestError:
        await event.reply("`Ho riscontrato un errore ma ho bannato uguale!`")
        return
    if reason:
        await event.reply(f"Bannato `{str(user.id)}` \nMotivo: {reason}")
    else:
        await event.reply(f"Bannato  `{str(user.id)}` !")


@tgbot.on(events.NewMessage(pattern="^/unbun(?: |$)(.*)"))
async def nothanos(event):
    userids = []
    noob = event.sender_id
    async for user in tgbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        userids.append(user.id)
    if noob not in userids:
        await event.reply("Non sei admin!")
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await event.reply("Non sono admin 🥺")
        return
    user = await get_user_from_event(event)
    user = user[0]
    if user:
        pass
    else:
        return
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await event.reply("`Ok l'ho sbannato gli diamo un altra chance.🚶`")
    except BadRequestError:
        await event.reply("`Non ho i permessi 🤭`")
        return



@tgbot.on(events.NewMessage(pattern="^/prumote(?: |$)(.*)"))
async def promote(event):
    userids = []
    noob = event.sender_id
    async for user in tgbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        userids.append(user.id)
    if noob not in userids:
        await event.reply("Non sei admin!")
        return
    """ con il comando .promote , promuove la persona indicata """
    # Get targeted chat
    chat = await event.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        await event.reply("Non sono admin 🥺")
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=False,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "coglione"  # Just in case.
    if user:
        pass
    else:
        return
    # Try to promote if current user is admin or creator
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
        await event.reply("`Promosso! FESTA`")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await event.reply("Non ho il permesso di promuovere 🤭")
        return


@tgbot.on(events.NewMessage(pattern="^/demote(?: |$)(.*)"))
async def demote(event):
    userids = []
    noob = event.sender_id
    async for user in tgbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        userids.append(user.id)
    if noob not in userids:
        await event.reply("Non sei admin!")
        return
    """ Con il comando .demote leva una promozione all'utente indicato """
    # Admin right check
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await event.reply("Non sono admin 🤭")
        return

    rank = "Coglione"  # dummy rank, lol.
    user = await get_user_from_event(event)
    user = user[0]
    if user:
        pass
    else:
        return

    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    # Edit Admin Permission
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        await event.reply("Non ho i permessi 🤔")
        return
    await event.reply("`Tolta una promozione a questo utente!`")

@tgbot.on(events.NewMessage(pattern="^/pin(?: |$)(.*)"))
async def pin(event):
    userids = []
    noob = event.sender_id
    async for user in tgbot.iter_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    ):
        userids.append(user.id)
    if noob not in userids:
        await event.reply("Non sei admin!")
        return
        """ Con il comando .pin fissa il messaggio indicato. """
    # Admin or creator check
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await event.reply("Devo essere amministratore 🤔")
        return

    to_pin = event.reply_to_msg_id

    if not to_pin:
        await event.reply("`Rispondi a un messaggio per fissarlo.`")
        return

    options = event.pattern_match.group(1)
    is_silent = True
    if options.lower() == "loud":
        is_silent = False
    try:
        await event.client(UpdatePinnedMessageRequest(event.to_id, to_pin, is_silent))
    except BadRequestError:
        await event.reply("Non ho i permessi giusti 🥺")
        return
    await event.reply("`Messaggio fissato!`")
    user = await get_user_from_id(msg.from_id, msg)

async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.reply("`Indica un utente tramite username, id o reply!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj
