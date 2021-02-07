# FermSense
Script for measuring different properties during beer fermentation from an external sensor.

This implementation currently supports temperature measurements but can be modified to use any other sensor. It has been tested on a Raspberry Pi 3 with an external DS18B20 sensor and a Raspberry Pi Zero W with an EnviroPHAT.

The script is meant to work together with the BrewBack API - https://github.com/busyfingers/BrewBack - where the data is sent after measuring. If the API cannot be reached, measurements are saved locally. Once the API is available, the locally stored values are sent to it. 
