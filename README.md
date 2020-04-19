# Azure Blob to Telegram

A Python Azure Function that uses the [FFmpeg library](https://ffmpeg.org/) to reduce the size of a video uploaded to Blob Storage and sends it to a [Telegram](https://telegram.org/) chat.

As you need to have the FFmpeg library installed to run it, this function should be [deployed as a container](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python).

## Steps to build, deploy and configure

1. Build the container image and upload it to your preferred image registry, like explained in the [build section](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python#build-the-container-image-and-test-locally)
2. Create an [Azure Function and all its resources](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python#create-supporting-azure-resources-for-your-function)
3. Create an Azure Storage Account with a container named **camerain**
4. Configure the mandatory fields
   * AzureWebJobsStorage
   * CameraDropFilesStorage
   * TELEGRAM_CHAT_ID
   * TELEGRAM_API_KEY
5. Enjoy (you may send some files to your Storage account camerain's folder)
