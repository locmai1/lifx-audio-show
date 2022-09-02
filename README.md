# Installing dependencies
```
pip install -r requirements.txt
```

# Setup and Configuration
1. Install Python and dependencies
2. Input order of lights into config.py in LIGHT_ORDER array
```
LIGHT_ORDER = ["LIFX Candle Color 6F675C", "LIFX Candle Color 64BC79"]
```
3. Run the following command in Terminal
```
python src/visualization.py
```
4. Choose which audio device (by index) to visualize
```
Audio Devices:
    Microphone (2- HyperX SoloCast) : 2 <-- index
    Speakers (Realtek High Definiti : 7 <-- index
    Realtek Digital Output (Realtek : 8 <-- index
Which to use: (index)
```
5. Choose mode and adjust sliders of properties
### Properties
Frequency
Brightness
Saturation
### Modes:
Energy
Scroll
Spectrum
Sine
Flat
### Controls:
Off
On
