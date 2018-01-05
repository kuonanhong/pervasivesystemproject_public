Pervasive Systems Project - Big Ear 2.0
============ 

The repository contains the code about the system developed for the pervasive systems course (Politecnico di Milano). 
It includes the code running on Raspberry pi, the RESTful server and a simple web application.

### Usage
+ Raspberry Pi
	+ Before everything, follow this guide in order to install everything is needed: [`ReSpeaker wiki`](http://wiki.seeed.cc/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/)
	+ Activate virtual environment create in the previous step
	+ Inside [`code`](code/) execute [`kws_doa.py`](code/kws_doa.py)

```
pi@raspberrypi:~ $ source ~/env/bin/activate
(env) pi@raspberrypi:~ $ cd ~/code
(env) pi@raspberrypi:~/code $ python kws_doa.py 
```
+ REST Server
	+  Inside [`rest-server`](rest-server/) execute [`server.py`](rest-server/server.py)
+ Web app
	+ Read the [`README`](web-app/README.md) inside the [`web-app`](web-app/) folder
	+ Execute the web application while the REST server is running 
	
+ Localization v2
	+ Inside the [`locazion-v2`](location-v2/) folder
	+ Jupyter notebook [`source_localization.ipynb`](location-v2/source_localization.ipynb) where localization is performed

    
### Code Structure
The code uses gstreamer-like [`elements`](code/voice_engine/element.py) which can be linked together as an audio pipeline.

The topology is:
```
Source --> ChannelPicker --> KWS
  |                           |
  V                           V
 DOA           Google Speech Recognition Service
 
```