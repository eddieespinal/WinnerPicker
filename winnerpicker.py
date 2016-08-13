#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by: Eddie Espinal
# Created on: August 6, 2016
# Copyright 2016 - EspinalLab, LLC
# www.4hackrr.com - Online Community For Engineers & Electronics Hobbyist!

import sys
import os
import subprocess
from gpiozero import LED, Button
import RPi.GPIO as GPIO
from sys import exit
from time import sleep
import pygame.mixer
from pygame.mixer import Sound
from signal import pause
from LCD import lcddriver
import json
from mailchimp import WinnerPicker
# MQTT
import paho.mqtt.client as mqtt
import threading
import datetime

from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

mqtt_host = parser.get('mqtt_server', 'host_ip')
mqtt_port = parser.get('mqtt_server', 'port')

GPIO.setmode(GPIO.BCM)
led = LED(14)
buttonLED = LED(21)

led.on()

# MQTT Setup
def on_connect(mosq, obj, rc):
	print("rc: " + str(rc))

def on_message(mosq, obj, msg):
	print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
	print("mid: " + str(mid))

def on_log(mosq, obj, level, string):
	print(string)

def send_payload(payload):
	mqttc.publish("WinnerPicker", payload)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.connect(mqtt_host, mqtt_port)
mqttc.loop_start()

pygame.mixer.init()

picker = WinnerPicker()

# Set the Raspberry PI volume to 90%
os.popen('amixer sset PCM,0 95%')

# NOTE: if audio doesn't play, run this command from termianl "amixer cset numid=3 1"
# Run this command to raise the volume up "amixer sset PCM,0 100%"
systemon = Sound("sounds/systemon.wav")
jackpot = Sound("sounds/jackpot2.wav")
picking = Sound("sounds/pickingwinner.wav")
failed = Sound("sounds/fail.wav")
winner_announcement = Sound("sounds/winner_announcement.wav")

# define the pins
ARCADE_BUTTON = 17

GPIO.setup(ARCADE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd = lcddriver.lcd()

def displayWinner(jsonString):
	if not jsonString:
		lcd.lcd_display_string("      ERROR     ", 1)
		lcd.lcd_display_string("EMAIL LIST EMPTY", 2)
		picking.stop()
		failed.paly()
		return

	json_dict = json.loads(jsonString)
	print json_dict

	resetLCD()
	lcd.lcd_display_string(" THE WINNER IS  ", 1)
	lcd.lcd_display_string("................", 2)
	winner_announcement.play()
	sleep(6.0)
	
	# Publish payload to MQTT channel
	send_payload(jsonString)

	jackpot.play()
	resetLCD()
	lcd.lcd_display_string(json_dict["name"], 1)
	lcd.lcd_display_string(json_dict["email"], 2)

	# update mailchimp and mark this user as a winner
	picker.updateSubscriber(json_dict["subscriber_id"])

	sleep(8.0)
	global output
	output = pickWinner()
	clearLCD()

def displayLCD():
	lcd.lcd_display_string("Choosing Winner!", 1)
	lcd.lcd_display_string("Please Wait.....", 2)
	picking.play()
	sleep(6.0)
	displayWinner(output)

def clearLCD():
	systemon.play()
	buttonLED.on()
	lcd.lcd_display_string("Press Button    ", 1)
	lcd.lcd_display_string("To Pick A Winner", 2)

def resetLCD():
	lcd.lcd_display_string("                ", 1)
	lcd.lcd_display_string("                ", 2)


def pickWinner():
	return picker.pickAWinner()

# Initialize and pull the data
lcd.lcd_display_string("Initializing    ", 1)
lcd.lcd_display_string("Please Wait.....", 2)
output = pickWinner()

sleep(0.5)

clearLCD()

while True:
	input_state = GPIO.input(ARCADE_BUTTON)
	if input_state == False:
		print('Button Pressed')
		buttonLED.off()
		displayLCD()
    	sleep(0.3)
