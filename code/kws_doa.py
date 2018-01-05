"""
Record audio from 4 mic array, and then search the keyword "snowboy".
After finding the keyword, Direction Of Arrival (DOA) is estimated.

The hardware is respeaker 4 mic array:
    https://www.seeedstudio.com/ReSpeaker-4-Mic-Array-for-Raspberry-Pi-p-2941.html
"""


import time
import urllib as url
import json,requests
import datetime
import base64
import pyaudio
import audioop
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_4mic_array import DOA
from pixels import pixels

#compute energy threshold for Activity detection
def compute_energy_threshold(channels = 4, chunk_size = 1024, sample_rate = 16000, sample_width = 2, duration = 3):
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        name = dev['name'].encode('utf-8')
        if dev['maxInputChannels'] == channels:
            device_index = i
            break
        
    stream = p.open(
        start=False,
        format=pyaudio.paInt16,
        input_device_index=device_index,
        channels = channels,
        rate = sample_rate,
        frames_per_buffer=int(sample_rate/100),
        input = True
    )
        
    stream.start_stream()
        
    seconds_per_buffer = (chunk_size + 0.0) / sample_rate
    elapsed_time = 0
    dynamic_energy_adjustment_damping = 0.15
    dynamic_energy_ratio = 1.5
    energy_threshold = 300
        

    # adjust energy threshold until a phrase starts
    while True:
        elapsed_time += seconds_per_buffer
        if elapsed_time > duration: break
        buffer = stream.read(chunk_size)
        energy = audioop.rms(buffer, sample_width)  # energy of the audio signal

        # dynamically adjust the energy threshold using asymmetric weighted average
        damping = dynamic_energy_adjustment_damping ** seconds_per_buffer  # account for different chunk sizes and rates
        target_energy = energy * dynamic_energy_ratio
        energy_threshold = energy_threshold * damping + target_energy * (1 - damping)
            
    stream.stop_stream() 
    p.terminate()        
    return energy_threshold

def main():
    print("Silence please ...")
    pixels.think()
    threshold = compute_energy_threshold()
    pixels.off()
    
    keywords = ["aiuto", "accendi la luce", "spegni la luce"]
    src = Source(rate=16000, channels=4, frames_size=320)
    ch1 = ChannelPicker(channels=4, pick=1)
    kws = KWS(keywords = keywords, energy_threshold = threshold)
    doa = DOA(rate=16000, chunks = 100)
    
    print("Sound energy threshold: ", threshold)
    
    src.link(ch1)
    ch1.link(kws)
    src.link(doa)

    def on_detected(keyword, wav_data):
        position = doa.get_direction()
        pixels.wakeup(position)
        print('detected {} at direction {}'.format(keyword, position).encode('utf8'))
        send_data(position, keyword, wav_data)
        
    def send_data(direction, command, wav_data):
        url = "http://192.168.100.1:8080/data"
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        jdata = { "id_mic": 1,"position": direction,"command":command, "ts": st, "audio_data": base64.b64encode(wav_data)}
        print("Post request toward", url)
        resp = requests.post(url, json = jdata)
        with open("record-demo.json",'w') as f:
            f.write(json.dumps(jdata))
    
    kws.set_callback(on_detected)

    src.recursive_start()
    
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
