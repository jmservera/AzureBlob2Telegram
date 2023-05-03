FROM mcr.microsoft.com/azure-functions/python:4-python3.10

LABEL version="1.2"

# add-apt-repository ppa:jonathonf/ffmpeg-4 && 
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot