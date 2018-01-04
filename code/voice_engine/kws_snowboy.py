# -*- coding: utf-8 -*-

"""
Keyword spotting using snowboy
"""

import os
import sys
import threading
import speech_recognition as sr
import pyaudio
import audioop


if sys.version_info[0] < 3:
    import Queue as queue
else:
    import queue

from .element import Element


class KWS(Element):
    def __init__(self, keywords = [], energy_threshold = 300, sensitivity=0.5):
        super(KWS, self).__init__()

        self.detector = sr.Recognizer()
        self.queue = queue.Queue()
        self.done = False
        self.listen = False
        self.counter = 0
        self.dataArr = []
        self.dataRecord = []
        self.keywords = keywords
        self.energy_threshold = energy_threshold
        self.on_detected = None

    def put(self, data):
        self.queue.put(data)
        self.counter += 1

    def start(self):
        self.done = False
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def stop(self):
        self.done = True

    def run(self):
        while not self.done:
            sample_width = 2
            data = self.queue.get()
            self.dataArr.append(data)
            if self.counter >= 20:
                frame_data = b"".join(self.dataArr)
                self.counter = 0
                energy = audioop.rms(frame_data, sample_width)
                if energy > self.energy_threshold:
                    self.listen = True
                    self.dataRecord = self.dataRecord + self.dataArr
                    self.dataArr = []
                if energy <= self.energy_threshold:
                    self.dataArr = []
                    if self.listen == True:
                        self.listen = False
                        print("Got it!! recognition in progress")
                        frame_data_record = b"".join(self.dataRecord)
                        audio_data = sr.AudioData(frame_data_record, 16000, sample_width)
                        self.dataRecord = []
                        with open("data-sended.wav","wb") as f:
                            f.write(audio_data.get_wav_data())
                        try:
                            ans = self.detector.recognize_google(audio_data, language = "it-IT").lower()
                            print(ans)
                            if any(word in ans for word in self.keywords):
                                if callable(self.on_detected):
                                    self.on_detected(ans,audio_data.get_wav_data() )
                        except sr.UnknownValueError:
                            print("Oooops, non ho capito!")
                        except sr.RequestError as e:
                            print("Impossibile effettuare la richiesta a Google Speech Recognition service!")
                            #Offline speech recocgnition....
            super(KWS, self).put(data)

    def set_callback(self, callback):
        self.on_detected = callback


def main():
    import time
    from voice_engine.source import Source

    src = Source()
    kws = KWS()

    src.link(kws)

    def on_detected(keyword):
        print('found {}'.format(keyword))

    kws.on_detected = on_detected

    kws.start()
    src.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    kws.stop()
    src.stop()


if __name__ == '__main__':
    main()
