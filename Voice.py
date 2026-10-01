import json, queue, threading, os
import sounddevice as sd
from vosk import Model, KaldiRecognizer

FRASES = {
    "américa del norte": "americanorte",
    "norteamérica": "americanorte",
    "sudamérica": "americasur",
    "américa del sur": "americasur",
    "europa": "europa",
    "asia": "asia",
    "áfrica": "africa",
    "oceanía": "oceania",
}

class Voice:
    def __init__(self, samplerate=16000, model_path="vosk-model-small-es-0.42"):
        if not os.path.isdir(model_path):
            raise SystemExit("El modelo VOSK no ha sido encontrado.")
        self._samplerate = samplerate
        self._model = Model(model_path)
        self._recognizer = KaldiRecognizer(
            self._model, samplerate, json.dumps(list(FRASES) + ["[unk]"], ensure_ascii=False)
        )
        self.audio = queue.Queue()
        self.result = queue.Queue()

    def start(self):
        threading.Thread(target=self._listen, daemon=True).start()

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio.put(bytes(indata))

    def _listen(self):
        with sd.RawInputStream(samplerate=self._samplerate, blocksize=8000,
                               dtype="int16", channels=1, callback=self._callback):
            while True:
                if self._recognizer.AcceptWaveform(self.audio.get()):
                    texto = json.loads(self._recognizer.Result())["text"]
                    if texto in FRASES:
                        self.result.put(FRASES[texto])

    def read_country(self):
        try:
            return self.result.get_nowait()
        except queue.Empty:
            return None