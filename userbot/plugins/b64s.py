import base64
from userbot.utils import friday_on_cmd, sudo_cmd, edit_or_reply


@friday.on(friday_on_cmd(pattern="bencode ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    kek = event.pattern_match.group(1)
    try:
        sample_string_bytes = kek.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        await event.edit(f"**ENCODED MESSAGE** - `{base64_string}`")
    except:
        await event.edit("SOM3THING W3NT WRONG !")

@friday.on(friday_on_cmd(pattern="bdecode ?(.*)"))
async def _(event):
    if event.fwd_from:
            return
    starky = event.pattern_match.group(1)
    try:
       base64_bytez = starky.encode("ascii")
       sample_string_bytez = base64.b64decode(base64_bytez)
       sample_strings = sample_string_bytez.decode("ascii")
       await event.edit(f"**DECODED STRING** : `{sample_strings}`")
    except:
       await event.edit("Can't Decoded Probably Due To Invalid String")

