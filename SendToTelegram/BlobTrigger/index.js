const {ffmpeg}=require("ffmpeg-stream");

module.exports = async function (context, inputBlob) {
    context.log("JavaScript blob trigger function processed blob \n Blob:", context.bindingData.blobTrigger, "\n Blob Size:", inputBlob.length, "Bytes");

    try {
        const converter = new ffmpeg();

        const input = converter.createInputStream({
            f: "image2pipe",
            vcodec: "h264",
          });

        input.read(inputBlob);
        // converter.createOutputStream({
        //     f:"gif",
        //     vcodec:"gif",
        //     vf:"scale=25:25"
        // });
        converter.createOutputToFile('/tmp/test.gif',{vcodec:"gif",vf:"scale=25:25"});

        await converter.run();
        context.log("Converted");

    } catch (e) {
        context.log(e);
        context.log(e.code);
        context.log(e.msg);
        throw(e);
    }

};