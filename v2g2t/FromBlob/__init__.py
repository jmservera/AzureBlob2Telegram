import logging

import azure.functions as func
import ffmpeg

import os
import subprocess as sp



def main(inputBlob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {inputBlob.name}\n"
                 f"Blob Size: {inputBlob.length} bytes")

    _,fullfilename=os.path.split(inputBlob.name)
    filename,_= os.path.splitext(fullfilename)
    with open(fullfilename,"wb") as download_file:
        while True:
            buf=inputBlob.read(4194304)
            download_file.write(bytes(buf))
            if len(buf)==0:
                break

    cmd_out = ['ffmpeg',
    '-y',
    '-i',fullfilename,
    '-an',
    '-vf','fps=10,scale=320:-1', # todo, scale from config
    '-c:v', 'h264', #'-preset:v', 'ultrafast',
    filename+"_b"+'.mp4']

    pipe = sp.Popen(cmd_out)

    pipe.wait()

    os.remove(fullfilename)
    

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
