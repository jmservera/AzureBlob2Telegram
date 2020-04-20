import azure.functions as func
import logging
import os
import subprocess as sp
import telegram
import tempfile

# environment variables
TELEGRAM_API_KEY = 'TELEGRAM_API_KEY'

TELEGRAM_CHAT_ID = 'TELEGRAM_CHAT_ID'

# default=True, set it to false if you want add notification to the messages
TELEGRAM_DISABLE_NOTIFICATION = 'TELEGRAM_DISABLE_NOTIFICATION'

# default=10
FFMPEG_FPS = 'FFMPEG_FPS'

# height is calculated from the width
FFMPEG_WIDTH = 'FFMPEG_WIDTH'

# default=True, set it to false if you want to send audio
FFMEG_NOAUDIO = 'FFMEG_NOAUDIO'


def main(inputBlob: func.InputStream):

    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {inputBlob.name}\n"
                 f"Blob Size: {inputBlob.length} bytes")

    # read environment variables
    telegram_token = os.getenv(TELEGRAM_API_KEY)
    if telegram_token is None:
        raise ValueError(f'{TELEGRAM_API_KEY} is missing')

    telegram_chat = os.getenv(TELEGRAM_CHAT_ID)
    if telegram_token is None:
        raise ValueError(f'{TELEGRAM_CHAT_ID} is missing')

    telegram_disable_notification = \
        bool(os.getenv(TELEGRAM_DISABLE_NOTIFICATION, True))

    fps = int(os.getenv(FFMPEG_FPS, 10))
    width = int(os.getenv(FFMPEG_WIDTH, 320))
    remove_audio = bool(os.getenv(FFMEG_NOAUDIO, True))
    audio = ''

    if remove_audio:
        audio = '-an'

    # set download path to the temp folder
    basepath = tempfile.gettempdir()

    _, fullfilename = os.path.split(inputBlob.name)
    fullfilename = os.path.join(basepath, fullfilename)

    cmd_out = ['ffmpeg',
               '-y',
               '-i', '-',  # use pipe
               audio,
               '-vf', f'fps={fps},scale={width}:-1',
               '-c:v', 'h264',
               fullfilename]

    pipe = sp.Popen(cmd_out, stdin=sp.PIPE)

    # write the blob stream to a file
    while True:
        buf = inputBlob.read(4194304)
        pipe.stdin.write(buf)
        if len(buf) == 0:
            break
    pipe.stdin.close()

    pipe.wait()

    os.path.getsize(fullfilename)
    logging.info(f'File reduced:\t{os.path.getsize(fullfilename)}')

    # send the reduced file to telegram

    with open(fullfilename, 'rb') as animation:
        bot = telegram.Bot(telegram_token)
        if remove_audio:
            bot.send_animation(
                telegram_chat, animation,
                disable_notification=telegram_disable_notification)
        else:
            bot.send_video(telegram_chat, animation)

    os.remove(fullfilename)
