const codeReader = new ZXing.BrowserMultiFormatReader();
const video = document.getElementById('preview');
const result = document.getElementById('result');

codeReader.listVideoInputDevices().then(devices => {
  const cam = devices[0].deviceId;

  codeReader.decodeFromVideoDevice(cam, video, (output, err) => {
    if (output) {
      result.textContent = output.text;
    }
  });
});