# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/node:2.0-appservice
FROM mcr.microsoft.com/azure-functions/node:2.0

# add-apt-repository ppa:jonathonf/ffmpeg-4 && 
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true 
    
COPY . /home/site/wwwroot

RUN cd /home/site/wwwroot && \
    npm install