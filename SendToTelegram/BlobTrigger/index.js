module.exports = async function (context, inputBlob) {
    context.log("JavaScript blob trigger function processed blob \n Blob:", context.bindingData.blobTrigger, "\n Blob Size:", inputBlob.length, "Bytes");
};