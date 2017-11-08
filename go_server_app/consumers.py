from channels.sessions import channel_session


@channel_session
def ws_connect(message):
    channel = message.reply_channel
    channel.send({"accept": True})


@channel_session
def ws_message(message):
    command = message.content['text']
    channel = message.reply_channel


@channel_session
def ws_disconnect(message):
    print(message)
