# WinnerPicker
This project is going to be used to choose random winners for my giveaways using the Mailchimp API to pull the data from the 4hackrr newsletter and randomly pick a winner.

# Dependecies
* You need to have an account setup with Mailchimp and a Newsletter in order for this script to work.

You need to install the python mailchimp client

`pip install mailchimp3`

Or follow the instructions here:

https://github.com/charlesthk/python-mailchimp

# Parts Needed
* Raspberry PI or Pi Zero
* Speaker - 3" Diameter - 4 Ohm 3 Watt - (https://www.adafruit.com/products/1314)
* Adafruit Mono 2.5W Class D Audio Amplifier - (https://www.adafruit.com/products/2130)
* Massive Arcade Button with LED - 100mm Green - (https://www.adafruit.com/products/1188)
* 16x2 LCD i2c - (https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=16x2+lcd+i2c)
* Headphone jack - Needed to get the audio from raspberry pi
* Green LED - not really needed but I used it to indicate the device is ON/OFF
* Wires Male/Female - (https://www.adafruit.com/products/1953)
* Sound Effects - I bought them from (https://audiojungle.net)

# Script Setup
* I'm using RASPBIAN JESSIE for this project. You can download it from here (https://www.raspberrypi.org/downloads/raspbian/)
* Once you have your raspbian setup, and internet working, you should clone this repository into `/home/pi/winnerpicker/` directory.
* Edit the config.ini file and add your own values. You need to have an account with Mailchimp and a Newsletter setup for this script to work properly.
* You should also setup your raspberry pi to automatically launch the script when it bootup. Todo so, you should follow the following steps:
* 1. Edit the /etc/profile file.  `sudo nano /etc/profile`
* 2. Add the following line to the end of the file `sudo /home/pi/winnerpicker/launchapp.sh &`
* 3. Save and exit the editor
* 4. Reboot your raspberry pi to test if it launches the app automatically. `sudo reboot`


