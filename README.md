# LIFX Audio Show

**Sync LIFX lights to realtime audio** from user's choice of microphone input. Visualization and audio analysis implemented from [audio-reactive-led-strip](https://github.com/scottlawsonbc/audio-reactive-led-strip)



## Requirements

Program is tested with `Python 3.10` with `LIFX Candle Color` bulbs. It also requires the following Python dependencies:  

* Numpy
* Scipy 
* PyQtGraph 
* PyQt5
* PyAudio 
* LifxLAN

### Installing Dependencies
The pip package manager is used to install the python dependencies. If `pip` is not found try using `python -m pip install` instead.
```
pip install -r requirements.txt
```
Installing on MacOS requires `portaudio` in addition to pyaudio which can be installed using:
```
brew install portaudio
``` 



## Setting up Lights

It's recommended to set up the lights in the **Official LIFX App** rather than Apple Home to avoid connectivity issues with program. Refer to `lights/data.txt` for information on the lights that David and I have already marked up. 

* '#' ---> What each light is marked with in accordance to its Label and HK Code
* 'Label' ---> Name you should put when setting up each light in the app
* 'HK Code' ---> The code needed to connect each light when prompted in the app

### Connecting Lights to WIFI:

The following should be done **to one light after another** to avoid confusion in light identification. It should also be done on the same WIFI that the program will be ran on.

1. Reset light by turning it on/off 5 times. On 5th time, light should cycle through red, green, and blue, meaning it's ready for connecting
2. In the LIFX app, click on the `+` then `New Device` then `New Light`
3. Click on corresponding light and enter its **HK Code** (refer to `lights/data.txt` and `#` on light) when prompted



## Setup and Configuration

1. Install Python and Python Dependencies
2. Configure how many lights to-be used by changing `NUM_LIGHTS` in `src/config.py`.
```
NUM_LIGHTS = 7   <--- Total lights to-be used
```
3. Configure the order of the light by adding the labels of each to `ORDER_LIGHTS` in `src/config.py`. Lights are positioned based on index in an array. Refer to `lights/data.txt` to get labels for each light.
```
ORDER_LIGHTS = ["LIFX Candle Color 6F3ED0",   <--- First position
                "LIFX Candle Color 64BF40",   
                "LIFX Candle Color 674622",
                "LIFX Candle Color 674613",
                "LIFX Candle Color 6F3BF1",
                "LIFX Candle Color 6F3080",
                "LIFX Candle Color 6F49BA"]   <--- Last position
```
4. Run audio visualization command. The visualization also starts the syncing process to the lights. **IMPORTANT:** If on MacOS, make sure the following command is ran in MacOS's terminal to get access to audio devices.
```
python src/visualization.py
```
5. Choose which audio device (by index) to retrieve audio from
```
Audio Devices:
    Microphone (2- HyperX SoloCast) : 2   <--- (index)
    Speakers (Realtek High Definiti : 7   <--- (index)
    Realtek Digital Output (Realtek : 8   <--- (index)

Which to use: (index)
```


## Controlling the Lights

Adjust the sliders to change the corresponding `properties` of all the lights. Click on different `modes` to switch between light patterns. Click each control options to change status of lights and visualization.

### Properties

* Frequency **(0 - 22050) hz**
* Brightness **(0 - 65535)**
* Saturation **(0 - 65535)**

### Modes:

* 'Energy' ---> strongest point in center
* 'Scroll' ---> wave effect from center
* 'Spectrum' ---> overall noise in audio
* 'Sine' ---> all lights follow a sine wave
* 'Flat' ---> shifts all light positions to the center of visualization **(modifies other modes)**

### Controls:

* 'Off' ---> turn all lights off
* 'On' ---> turn all lights on
* 'Kill' ---> shut down visualization and turns lights off
