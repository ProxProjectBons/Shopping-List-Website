const codeReader = new ZXing.BrowserMultiFormatReader();
const video = document.getElementById('preview');
const result = document.getElementById('result');

// Array für alle gescannten Codes
const scannedItems = [];

// Optional: UL-Element für die Liste
const list = document.getElementById('scan-list');

codeReader.listVideoInputDevices().then(devices => {
  const cam = devices[0].deviceId;

  codeReader.decodeFromVideoDevice(cam, video, (output, err) => {
    if (output) {
      const text = output.text;

      // Ausgabe im UI
      result.textContent = text;

      // In Array speichern
      scannedItems.push(text);

      // In Liste anzeigen
      const li = document.createElement('li');
      li.textContent = text;
      list.appendChild(li);

      console.log(scannedItems);
    }
  });
});
