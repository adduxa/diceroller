#!/usr/bin/env python3

import pyrogram

# Using Pyrogram -- Telegram MTProto API Framework for Python
# https://github.com/pyrogram/pyrogram

# Pyrogram quick start guide
# https://docs.pyrogram.org/intro/quickstart

# Get your own Telegram API key from https://my.telegram.org/apps
api_id = API_ID
api_hash = API_HASH

app = pyrogram.Client("my_account", api_id, api_hash)
app.start()

# Fetching all supported dice emoji with help.GetAppConfig
# https://core.telegram.org/api/config#client-configuration

app_config = app.send(pyrogram.api.functions.help.GetAppConfig())

print("All supported dice emoji:")
for field in app_config.value:
    if field.key == "emojies_send_dice":
        for emoji in field.value.value:
            print(emoji.value)

# All currently suported dice emoji with names
dices = [
    {
        "emoji": "🎲",
        "name": "dice",
    }, {
        "emoji": "🎯",
        "name": "dart",
    }, {
        "emoji": "🏀",
        "name": "ball",
    }, {
        "emoji": "⚽️",
        "name": "soccer",
    }, {
        "emoji": "⚽️",
        "name": "soccer2",
    }, {
        "emoji": "🎰",
        "name": "slots",
    }, {
        "emoji": "🎳",
        "name": "bowling",
    },
]

# Download them all
for dice in dices:
    dice_emoji = dice['emoji']
    dice_name = dice['name']

    # How to request sticker documents for a given emoji
    # https://core.telegram.org/api/dice
    print("Downloading animations for a %s emoji %s" % (dice_name, dice_emoji))

    # Pyrogram doen not have functions for downloading sticker sets' documents
    # We'll use Raw Functions and Types to form and execute TL-schema method calls directly to Telegram API
    # https://docs.pyrogram.org/telegram/functions/
    # https://docs.pyrogram.org/telegram/types/

    # Constructing InputStickerSet with inputStickerSetDice
    # https://core.telegram.org/constructor/inputStickerSetDice
    input_sticker_set = pyrogram.api.types.InputStickerSetDice(emoticon=dice_emoji)

    # Constructing TL-method messages.getStickerSet using InputStickerSet
    # https://core.telegram.org/method/messages.getStickerSet
    get_sticker_set = pyrogram.api.functions.messages.GetStickerSet(stickerset=input_sticker_set)

    # Calling Telegram API with RawFunction
    # https://docs.pyrogram.org/api/methods/send
    #
    # Returns Messages.StickerSet object
    # https://core.telegram.org/constructor/messages.stickerSet
    sticker_set = app.send(get_sticker_set)

    # Message.StickerSet.packs has StickerPack objects with emoticon and document ids of the animation Document objects
    # https://core.telegram.org/constructor/messages.stickerSet
    for pack in sticker_set.packs:
        print("Got document %d for '%s'" % (pack.documents[0], pack.emoticon))
        # Could be more than one Document for each emoticon, but not in our case

    # Each Document can be downloaded with upload.getFile method resulting upload.File
    # https://core.telegram.org/api/files#downloading-files
    #
    # The file download operation may return an upload.fileCdnRedirect constructor
    # In our case it does, so these instructions must be followed for downloading CDN files:
    # https://core.telegram.org/cdn

    # Starting from here, we can use implemented Pyrogram functions for dealing with Document downloading
    for i in range(len(sticker_set.documents)):
        sticker_set_document = sticker_set.documents[i]
        filename = "%s_%d.tgs" % (dice_name, i)

        print("Downloading document %d as '%s'" % (sticker_set_document.id, filename))

        # Constructing Pyrogram.Document from TL-schema's Document using private not documented constructor
        # pyrogram/client/types/messages_and_media/document.py
        document = pyrogram.Document._parse(client=app, document=sticker_set_document, file_name=filename)

        # Downloading Pyrogram.Document with Pyrogram.download_media()
        # https://docs.pyrogram.org/api/methods/download_media
        app.download_media(message=document)


# Stopping the Pyrogram client
app.stop()
