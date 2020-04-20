# Azure Blob to Telegram

![Python application](https://github.com/jmservera/AzureBlob2Telegram/workflows/Python%20application/badge.svg)

A Python Azure Function that uses the [FFmpeg library](https://ffmpeg.org/) to reduce the size of a video uploaded to Blob Storage and sends it to a [Telegram](https://telegram.org/) chat.

As you need to have the FFmpeg library installed to run it, this function should be [deployed as a container](https://docs.microsoft.com/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python).

## What do I need

* An Azure Storage account with a container named **camerain** where you drop your .mp4 files.
* A [Telegram Bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot) API id.
* Any system that drops .mp4 files into the Azure Storage Account

## Steps to build, deploy and configure

1. Build the container image and upload it to your preferred image registry. You can follow the [build container image](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python#build-the-container-image-and-test-locally) tutorial. In my case I used [Azure Container Registry](https://azure.microsoft.com/services/container-registry/)
2. Create an [Azure Function and all its resources](https://docs.microsoft.com/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python#create-supporting-azure-resources-for-your-function).
3. Create an Azure Storage Account with a container named **camerain**, or you can change it in the [function.json](./video2telegramfunction/FromBlob/function.json) *path* property, before building the container.
4. Configure the mandatory fields
   * AzureWebJobsStorage
   * CameraDropFilesStorage
   * TELEGRAM_CHAT_ID
   * TELEGRAM_API_KEY
5. Enjoy (you may send some files to your Storage account camerain's folder)

## Parameters

There's some additional parameters that you may use to influence the way video is scaled, here are all the configuration parameters for this container:

* **AzureWebJobsStorage**: mandatory, used for task sincronization by the Azure Functions Platform
* **CameraDropFilesStorage**: mandatory, needs to have a *camerain* container where you drop the .mp4 files
* **TELEGRAM_API_KEY**: mandatory, the Bot API Key from Telegram
* **TELEGRAM_CHAT_ID**: mandatory, the ID of the chat where you want to send the video
* **TELEGRAM_DISABLE_NOTIFICATION**: default=True, set it to false if you want add notification to the messages
* **FFMPEG_FPS**: default=10
* **FFMPEG_WIDTH**: default=320, height is calculated from the width
* **FFMEG_NOAUDIO**: default=True, set it to false if you want to send audio
