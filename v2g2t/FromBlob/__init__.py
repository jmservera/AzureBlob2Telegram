import logging

import azure.functions as func
import ffmpeg

import os
import tempfile
import subprocess as sp

import telegram

# environment variables
TELEGRAM_API_KEY='TELEGRAM_API_KEY'
TELEGRAM_CHAT_ID='TELEGRAM_CHAT_ID'
FFMPEG_FPS='FFMPEG_FPS'
FFMPEG_WIDTH='FFMPEG_WIDTH' # height is calculated from the width
FFMEG_NOAUDIO='FFMEG_NOAUDIO' # default=True, set it to false if you want to send audio

def main(inputBlob: func.InputStream):

    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {inputBlob.name}\n"
                 f"Blob Size: {inputBlob.length} bytes")

    # read environment variables
    telegram_token=os.getenv(TELEGRAM_API_KEY)
    if telegram_token==None:
        raise ValueError(f'{TELEGRAM_API_KEY} is missing')
    
    telegram_chat=os.getenv(TELEGRAM_CHAT_ID)
    if telegram_token==None:
        raise ValueError(f'{TELEGRAM_CHAT_ID} is missing')


    fps=int(os.getenv(FFMPEG_FPS,10))
    width=int(os.getenv(FFMPEG_WIDTH,320))
    remove_audio=bool(os.getenv(FFMEG_NOAUDIO,True))
    audio=''
    if remove_audio:
        audio='-an'

    # set download path to the temp folder
    basepath=tempfile.gettempdir()

    _,fullfilename=os.path.split(inputBlob.name)    
    fullfilename=os.path.join(basepath,fullfilename)
    reducedfilename,extension= os.path.splitext(fullfilename)
    reducedfilename=os.path.join(basepath,f'{reducedfilename}_b{extension}')

    # write the blob stream to a file
    with open(fullfilename,"wb") as download_file:
        while True:
            buf=inputBlob.read(4194304)
            download_file.write(bytes(buf))
            if len(buf)==0:
                break

    cmd_out = ['ffmpeg',
    '-y',
    '-i',fullfilename,
    audio,
    '-vf',f'fps={fps},scale={width}:-1', # todo, scale from config
    '-c:v', 'h264', #'-preset:v', 'ultrafast',
    reducedfilename]

    pipe = sp.Popen(cmd_out)

    pipe.wait()


    os.path.getsize(reducedfilename)
    logging.info(f'File reduced:\n\t{fullfilename}\t{os.path.getsize(fullfilename)}\n\t{reducedfilename}\t{os.path.getsize(reducedfilename)}')
    os.remove(fullfilename)

    # send the reduced file to telegram
    
    with open(reducedfilename,'rb') as animation:
        bot=telegram.Bot(telegram_token)
        if remove_audio:
            bot.send_animation(telegram_chat,animation)
        else:
            bot.send_video(telegram_chat,animation)

    os.remove(reducedfilename)
    # cmd_out = ['ffmpeg',
    #         '-y',  # (optional) overwrite output file if it exists
    #         '-f', 'image2pipe',
    #         '-vcodec', 'h264',
    #         '-i', '-',  # The input comes from a pipe
    #         '-vcodec', 'gif',
    #         '-f','image2pipe',
    #         '-o','-']



    # pipe = sp.Popen(cmd_out, stdin=sp.PIPE)
    # output, _ = pipe.communicate()

    # # for screenshot in screenshot_list:
    # #     im = Image.open(BytesIO(base64.b64decode(screenshot)))
    # #     im.save(pipe.stdin, 'PNG')

    # pipe.stdin.close()
    # pipe.wait()
