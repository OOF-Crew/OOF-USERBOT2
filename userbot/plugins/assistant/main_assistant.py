#    Copyright (C) Midhun KM 2020
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
# 
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from telethon import events, custom, Button
from telethon.tl.types import (
    Channel,
    Chat,
    User
)

import emoji
import asyncio
from googletrans import Translator
import re
import io
from math import ceil
from userbot.plugins import inlinestats
from telethon import custom, events, Button
from userbot import CMD_LIST
from userbot.utils import friday_on_cmd, edit_or_reply, sudo_cmd
from telethon.utils import get_display_name
from userbot.utils import friday_on_cmd, sudo_cmd
from userbot.uniborgConfig import Config
from telethon import events
from datetime import datetime
from userbot.utils import friday_on_cmd, edit_or_reply, sudo_cmd
import time
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from userbot import Lastupdate, bot
from userbot.plugins.sql_helper.botusers_sql import add_me_in_db, his_userid
from userbot.plugins.sql_helper.idadder_sql import add_usersid_in_db, get_all_users, already_added
from userbot.plugins.sql_helper.blacklist_assistant import add_nibba_in_db, get_all_nibba, is_he_added, removenibba

@tgbot.on(events.NewMessage(pattern="^/start"))
async def start(event):
    starkbot = await tgbot.get_me()
    bot_id = starkbot.first_name
    bot_username = starkbot.username
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.user.first_name
    vent = event.chat_id
    starttext = (f"Hey ciao, {firstname} ! Sono felice di parlare con te, Io sono {bot_id}, ovvero il bot aiutante del mio [Padrone](tg://user?id={bot.uid}) \nPuoi parlare con il mio padrone tramite questo bot.
    if event.sender_id == bot.uid:
        await tgbot.send_message(
           vent,
           message=f"hey, io sono {bot_id}, Il tuo assistente ! \nCosa ti serve ? cercherò di aiutarti :)",
           buttons = [
           [custom.Button.inline("Lista utenti 🔥", data="users")],
           [custom.Button.inline("I miei comandi", data="gibcmd")],
           [Button.url("Aggiungimi a un gruppo 👥", f"t.me/{bot_username}?startgroup=true")]
            ]
           )
    else:
        if already_added(event.sender_id):
            pass
        elif not already_added(event.sender_id):
            add_usersid_in_db(
                event.sender_id
             )
        await tgbot.send_message(
           event.chat_id,
           message=starttext,
           link_preview=False,
           buttons = [
           [Button.url("Marvyn ❓", "t.me/MarvynSTAR")],
           [Button.url("Doggy ❓", "t.me/Doggy_cheems")]
       ]
      )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"users")))
async def users(event):
        if event.query.user_id == bot.uid:
             await event.delete()
             total_users = get_all_users()
             users_list = "List Of Total Users In Bot. \n\n"
             for starked in total_users:
                 users_list += ("==> {} \n").format(int(starked.chat_id))
             with io.BytesIO(str.encode(users_list)) as tedt_file:
                 tedt_file.name = "userlist.txt"
                 await tgbot.send_file(
                     event.chat_id,
                     tedt_file,
                     force_document=True,
                     caption="Ecco gli utenti che mi hanno avviato.",
                     allow_cache=False
                     )
        else:
            pass
@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"gibcmd")))
async def users(event):
         await event.delete()
         grabon = "Ecco i miei comandi \n➤ /start - Controlla se sono online \n➤ /ping - Pong! \n➤ /tr <lang-code> \n➤ /broadcast - Scrivi un messaggioda mandare a tutti gli utenti che mi hanno avviato \n➤ /id - Mostra gli id degli utenti. \n➤ /addnote - Aggiungi una nota \n➤ /notes - Mostra le note \n➤ /rmnote - Rimuovi una nota \n➤ /alive - Sono online? \n➤ /bun - Banna un utente (solo gruppi). \n➤ /unbun - Sbanna un utente (solo gruppi) \n➤ /prumote - Promuove un utente \n➤ /demute - Declassa un utente \n➤ /pin - Fissa un messaggio\n➤ /stats - Mostra gli utenti che mi hanno avviato"
         await tgbot.send_message(
             event.chat_id,
             grabon
         )
             

# Bot Permit.
@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def all_messages_catcher(event):
    if is_he_added(event.sender_id):
        return
    if event.raw_text.startswith("/"):
        pass
    elif event.sender_id == bot.uid:
        return
    else:
        sender = await event.get_sender()
        chat_id = event.chat_id
        sed = await event.forward_to(bot.uid)
# Add User To Database ,Later For Broadcast Purpose
# (C) @SpecHide
        add_me_in_db(
            sed.id,
            event.sender_id,
            event.id
        )



@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def sed(event):
    msg = await event.get_reply_message()
    if not msg.text:
        return
    real_nigga = msg.id
    msg_s = event.raw_text
    user_id, reply_message_id = his_userid(
        msg.id
        )
    if event.sender_id == bot.uid:
        if event.raw_text.startswith("/"):
            pass
        else:
            await tgbot.send_message(
            user_id,
            msg_s
            )

# broadcast
@tgbot.on(events.NewMessage(pattern="^/broadcast ?(.*)", func=lambda e: e.sender_id == bot.uid))
async def sedlyfsir(event):
    msgtobroadcast = event.pattern_match.group(1)
    userstobc = get_all_users()
    error_count = 0
    sent_count = 0
    for starkcast in userstobc:
        try:
            sent_count += 1
            await tgbot.send_message(int(starkcast.chat_id), msgtobroadcast)
            await asyncio.sleep(0.2)
        except Exception as e:
            try:
                 logger.info(f"Error : {error_count}\nError : {e} \nUsers : {chat_id}"
                 )
            except:
                 pass
    await tgbot.send_message(
        event.chat_id,
        f"Broadcast Done in {sent_count} Group/Users and I got {error_count} Error and Total Number Was {len(userstobc)}"
        )


@tgbot.on(events.NewMessage(pattern="^/stats ?(.*)", func=lambda e: e.sender_id == bot.uid))
async def starkisnoob(event):
    starkisnoob = get_all_users()
    await event.reply(f"**Stats Of Your Bot** \nTotal Users In Bot => {len(starkisnoob)}")
    
@tgbot.on(events.NewMessage(pattern="^/help", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    grabonx = "Hello Here Are Some Commands \n➤ /start - Check if I am Alive \n➤ /ping - Pong! \n➤ /tr <lang-code> \n➤ /broadcast - Sends Message To all Users In Bot \n➤ /id - Shows ID of User And Media. \n➤ /addnote - Add Note \n➤ /notes - Shows Notes \n➤ /rmnote - Remove Note \n➤ /alive - Am I Alive? \n➤ /bun - Works In Group , Bans A User. \n➤ /unbun - Unbans A User in Group \n➤ /prumote - Promotes A User \n➤ /demute - Demotes A User \n➤ /pin - Pins A Message \n➤ /stats - Shows Total Users In Bot"
    await event.reply(grabonx)
    
@tgbot.on(events.NewMessage(pattern="^/block ?(.*)", func=lambda e: e.sender_id == bot.uid))
async def starkisnoob(event):
    if event.sender_id == bot.uid:
        msg = await event.get_reply_message()
        real_nigga = msg.id
        msg_s = event.raw_text
        user_id, reply_message_id = his_userid(
        msg.id
        )
    if is_he_added(user_id):
        await event.reply("Already Blacklisted")
    elif not is_he_added(user_id):
        add_nibba_in_db(
            user_id
          )
        await event.reply("Blacklisted This Dumb Person")
        await tgbot.send_message(user_id, "You Have Been Blacklisted And You Can't Message My Master Now.")

@tgbot.on(events.NewMessage(pattern="^/unblock ?(.*)", func=lambda e: e.sender_id == bot.uid))
async def starkisnoob(event):
    if event.sender_id == bot.uid:
        msg = await event.get_reply_message()
        real_nigga = msg.id
        msg_s = event.raw_text
        user_id, reply_message_id = his_userid(
        msg.id
        )
    if not is_he_added(user_id):
        await event.reply("Not Even. Blacklisted 🤦🚶")
    elif is_he_added(user_id):
        removenibba(
            user_id
          )
        await event.reply("DisBlacklisted This Dumb Person")
        await tgbot.send_message(user_id, "Congo! You Have Been Unblacklisted By My Master.")
