"""
Written by totalJTM
Main micropython program to handle the graduation cap functionality
This program can be controlled through REPL by calling commands (in this file and in GradCap class)
"""

import machine
import random
from secrets import Secrets as secrets
from gradcap import GradCap
from micropython import const
import micropython
from time import sleep, sleep_ms

#clean up heap
gc.collect()

#function to print the number of allocated and free bytes in RAM
def get_ram():
	alloc = gc.mem_alloc()
	free = gc.mem_free()
	print("Allocated Mem: " + str(alloc) + " | Free Mem: " + str(free))

#pre-programmed sprites the program will iter through
#sprites are 14 rows by 14 columns, each index has a number that references an index in the colors array "in GradCap class"
sprites = [
		#sprite 0, combined TU
		[[05,05,05,05,05,05,05,05,05,00,00,00,00,00],\
		[05,00,00,00,05,00,00,00,05,00,00,00,00,00],\
		[05,00,00,00,05,00,00,00,05,00,00,00,00,00],\
		[00,00,00,00,05,00,00,00,00,00,00,00,00,00],\
		[00,00,00,00,05,00,00,00,00,00,00,00,00,00],\
		[00,00,00,00,05,04,04,04,00,00,00,04,04,04],\
		[00,00,00,00,05,00,04,00,00,00,00,00,04,00],\
		[00,00,00,00,05,00,04,00,00,00,00,00,04,00],\
		[00,00,05,05,05,05,05,00,00,00,00,00,04,00],\
		[00,00,00,00,00,00,04,00,00,00,00,00,04,00],\
		[00,00,00,00,00,00,04,00,00,00,00,00,04,00],\
		[00,00,00,00,00,00,04,00,00,00,00,00,04,00],\
		[00,00,00,00,00,00,00,04,00,00,00,04,00,00],\
		[00,00,00,00,00,00,00,00,04,04,04,00,00,00]]\
		,\
		#sprite 1, combined TU with changing background
		#[[05,05,05,05,05,05,05,05,05,06,06,06,06,06],\
		#[05,06,06,06,05,06,06,06,05,06,06,06,06,06],\
		#[05,06,06,06,05,06,06,06,05,06,06,06,06,06],\
		#[06,06,06,06,05,06,06,06,06,06,06,06,06,06],\
		#[06,06,06,06,05,06,06,06,06,06,06,06,06,06],\
		#[06,06,06,06,05,04,04,04,06,06,06,04,04,04],\
		#[06,06,06,06,05,06,04,06,06,06,06,06,04,06],\
		#[06,06,06,06,05,06,04,06,06,06,06,06,04,06],\
		#[06,06,05,05,05,05,05,06,06,06,06,06,04,06],\
		#[06,06,06,06,06,06,04,06,06,06,06,06,04,06],\
		#[06,06,06,06,06,06,04,06,06,06,06,06,04,06],\
		#[06,06,06,06,06,06,04,06,06,00,06,06,04,06],\
		#[06,06,06,06,06,06,06,04,06,06,06,04,06,06],\
		#[06,06,06,06,06,06,06,06,04,04,04,06,06,06]]\
		#,\
		#sprite 1, TU EE 21
		[[05,05,05,05,05,05,05,00,00,00,00,00,00,00],
		[05,00,00,05,00,00,05,00,02,02,00,02,02,00],
		[00,00,00,05,00,00,00,00,02,00,00,02,00,00],
		[00,00,00,05,00,00,00,00,02,02,00,02,02,00],
		[00,00,00,05,00,00,00,00,02,00,00,02,00,00],
		[00,00,00,05,00,00,00,00,02,02,00,02,02,00],
		[00,05,05,05,05,05,00,00,00,00,00,00,00,00],
		[00,00,00,00,00,00,00,05,00,00,00,00,00,05],
		[00,02,02,00,00,02,00,05,00,00,00,00,00,05],
		[00,00,00,02,00,02,00,05,00,00,00,00,00,05],
		[00,00,02,00,00,02,00,05,00,00,00,00,00,05],
		[00,02,00,00,00,02,00,05,00,00,00,00,00,05],
		[00,02,02,02,00,02,00,00,05,00,00,00,05,00],
		[00,00,00,00,00,00,00,00,00,05,05,05,00,00]]
		,
		#sprite 2	GR AD
		[[00,00,05,05,05,00,00,00,02,02,02,02,00,00],
		[00,05,00,00,00,05,00,00,02,00,00,00,02,00],
		[05,00,00,00,00,00,00,00,02,00,00,00,02,00],
		[05,00,00,00,00,00,00,00,02,02,02,02,00,00],
		[05,00,00,00,05,05,00,00,02,00,02,00,00,00],
		[00,05,00,00,00,05,00,00,02,00,00,02,00,00],
		[00,00,05,05,05,00,00,00,02,00,00,02,00,00],
		[00,00,02,02,00,00,00,00,05,05,05,00,00,00],
		[00,02,00,00,02,00,00,00,05,00,00,05,00,00],
		[02,00,00,00,00,02,00,00,05,00,00,00,05,00],
		[02,00,02,02,00,02,00,00,05,00,00,00,05,00],
		[02,02,00,00,02,02,00,00,05,00,00,00,05,00],
		[02,00,00,00,00,02,00,00,05,00,00,05,00,00],
		[02,00,00,00,00,02,00,00,05,05,05,00,00,00]]
		,
		#sprite 3 flame
		[[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		[00,00,00,07,00,00,00,07,00,00,00,00,00,00],
		[00,00,07,00,00,00,07,00,00,00,07,00,00,00],
		[00,00,07,07,00,00,00,07,00,07,00,00,00,00],
		[00,07,07,08,07,00,00,07,00,00,07,00,00,00],
		[00,00,07,08,07,07,00,00,07,00,00,07,00,00],
		[00,00,00,07,08,08,08,07,07,00,00,07,00,00],
		[00,00,00,07,08,09,08,08,07,07,07,00,00,00],
		[00,00,07,08,09,08,09,08,08,07,08,07,07,00],
		[00,00,07,07,08,09,08,09,08,09,08,07,07,00],
		[00,00,07,08,07,08,09,08,09,08,07,08,07,00],
		[00,00,00,07,08,07,08,07,08,07,08,07,00,00],
		[00,00,00,00,07,07,07,07,07,07,07,00,00,00],
		[00,00,00,00,00,00,00,00,00,00,00,00,00,00]]
		,
		#sprite 4 T white
		[[04,04,04,04,04,04,04,04,04,04,04,04,04,04],
		[04,00,00,00,00,00,00,00,00,00,00,00,00,04],
		[04,00,00,00,00,00,00,00,00,00,00,00,00,04],
		[04,00,00,04,04,04,00,00,04,04,04,00,00,04],
		[04,00,00,04,00,04,00,00,04,00,04,00,00,04],
		[00,00,00,00,00,04,00,00,04,00,00,00,00,00],
		[00,00,00,00,00,04,00,00,04,00,00,00,00,00],
		[00,00,00,00,00,04,00,00,04,00,00,00,00,00],
		[00,00,00,00,00,04,00,00,04,00,00,00,00,00],
		[00,00,00,00,00,04,00,00,04,00,00,00,00,00],
		[00,00,00,04,04,04,00,00,04,04,04,00,00,00],
		[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		[00,00,00,04,04,04,04,04,04,04,04,00,00,00]]
		,
		#sprite 5 U white
		[[04,00,00,04,00,00,00,00,00,00,04,00,00,04],
		[04,00,00,04,00,00,00,00,00,00,04,00,00,04],
		[04,00,00,04,00,00,00,00,00,00,04,00,00,04],
		[04,00,00,04,00,00,00,00,00,00,04,00,00,04],
		[04,00,00,04,00,00,00,00,00,00,04,00,00,04],
		[04,00,00,04,00,00,00,00,00,00,04,00,00,04],
		[04,00,00,04,00,00,00,00,00,00,04,00,00,04],
		[04,00,00,04,00,00,00,00,00,00,04,00,00,04],
		[04,00,00,04,00,00,00,00,00,00,04,00,00,04],
		[04,00,00,00,04,00,00,00,00,04,00,00,00,04],
		[00,04,00,00,00,04,04,04,04,00,00,00,04,00],
		[00,00,04,00,00,00,00,00,00,00,00,04,00,00],
		[00,00,00,04,00,00,00,00,00,00,04,00,00,00],
		[00,00,00,00,04,04,04,04,04,04,00,00,00,00]]
		,
		#sprite 6 T cherry
		[[05,05,05,05,05,05,05,05,05,05,05,05,05,05],
		[05,00,00,00,00,00,00,00,00,00,00,00,00,05],
		[05,00,00,00,00,00,00,00,00,00,00,00,00,05],
		[05,00,00,05,05,05,00,00,05,05,05,00,00,05],
		[05,00,00,05,00,05,00,00,05,00,05,00,00,05],
		[00,00,00,00,00,05,00,00,05,00,00,00,00,00],
		[00,00,00,00,00,05,00,00,05,00,00,00,00,00],
		[00,00,00,00,00,05,00,00,05,00,00,00,00,00],
		[00,00,00,00,00,05,00,00,05,00,00,00,00,00],
		[00,00,00,00,00,05,00,00,05,00,00,00,00,00],
		[00,00,00,05,05,05,00,00,05,05,05,00,00,00],
		[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		[00,00,00,05,05,05,05,05,05,05,05,00,00,00]]
		,
		#sprite 7 U cherry
		[[05,00,00,05,00,00,00,00,00,00,05,00,00,05],
		[05,00,00,05,00,00,00,00,00,00,05,00,00,05],
		[05,00,00,05,00,00,00,00,00,00,05,00,00,05],
		[05,00,00,05,00,00,00,00,00,00,05,00,00,05],
		[05,00,00,05,00,00,00,00,00,00,05,00,00,05],
		[05,00,00,05,00,00,00,00,00,00,05,00,00,05],
		[05,00,00,05,00,00,00,00,00,00,05,00,00,05],
		[05,00,00,05,00,00,00,00,00,00,05,00,00,05],
		[05,00,00,05,00,00,00,00,00,00,05,00,00,05],
		[05,00,00,00,05,00,00,00,00,05,00,00,00,05],
		[00,05,00,00,00,05,05,05,05,00,00,00,05,00],
		[00,00,05,00,00,00,00,00,00,00,00,05,00,00],
		[00,00,00,05,00,00,00,00,00,00,05,00,00,00],
		[00,00,00,00,05,05,05,05,05,05,00,00,00,00]]
		,
		#sprite 8 cherries
		[[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		[00,00,00,00,00,00,00,00,01,01,01,00,00,00],
		[00,00,00,00,00,00,00,01,01,00,00,00,00,00],
		[00,00,00,00,00,00,01,01,00,01,01,01,00,00],
		[00,00,00,00,00,01,00,01,00,00,00,00,00,00],
		[00,00,00,00,00,01,00,01,00,00,00,00,00,00],
		[00,00,00,02,02,02,00,00,01,00,00,00,00,00],
		[00,00,02,04,04,05,02,00,02,02,02,00,00,00],
		[00,02,04,05,05,05,05,02,04,04,05,02,00,00],
		[00,02,05,05,05,05,02,04,05,05,05,05,02,00],
		[00,00,02,05,05,05,02,05,05,05,05,05,02,00],
		[00,00,00,02,02,02,00,02,05,05,05,02,00,00],
		[00,00,00,00,00,00,00,00,02,02,02,00,00,00],
		[00,00,00,00,00,00,00,00,00,00,00,00,00,00]]
		,
		#sprite 9 owl
		[[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		[00,00,00,00,05,00,00,00,00,05,00,00,00,00],
		[00,00,00,05,02,00,00,00,00,02,05,00,00,00],
		[00,00,05,05,05,05,05,05,05,05,05,05,00,00],
		[00,05,05,02,05,05,05,05,05,05,02,05,05,00],
		[00,05,00,00,02,05,05,05,05,02,00,00,05,00],
		[00,05,05,09,00,02,05,05,02,00,09,05,05,00],
		[00,05,02,02,00,00,05,05,00,00,02,02,05,00],
		[00,05,05,02,02,02,02,02,02,02,02,05,05,00],
		[00,00,05,05,05,06,06,06,06,05,05,05,00,00],
		[00,00,00,05,05,05,06,06,05,05,05,00,00,00],
		[00,00,00,00,00,05,05,05,05,00,00,00,00,00],
		[00,00,00,00,00,00,05,05,00,00,00,00,00,00],
		[00,00,00,00,00,00,00,00,00,00,00,00,00,00]]
		#,
		#empty array
		#[[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00],
		#[00,00,00,00,00,00,00,00,00,00,00,00,00,00]]
		]

#create instance of GradCap class
cap = GradCap()

#clean up heap
gc.collect()

#connect to a wifi network
def do_connect(ssid, pwd):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
 
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
 
# Attempt to connect to WiFi network
do_connect(secrets.WIFI_SSID, secrets.WIFI_PSWD)

#clean up heap
gc.collect()

#create instance of discord bot class and pass in bot token
from mpdiscordbot import MP_DiscordBot
discbot = MP_DiscordBot(secrets.BOT_TOKEN)

#define bot identifier string (number and <@>)
bot_identifier = ['<@!837072927030771752>','<@837072927030771752>']

#creat instance of text filter
from textfilter import TextFilter
tfilt = TextFilter()

import ujson as json

#define some variables for use in normal_operation()
stored_messages = []
last_message_id = None
last_sprite_index = 0

#define the different channels I want to connect to
channel_details = [ {'name':'EE_Discord','id':615577149595713560},
					{'name':'SD_Discord','id':747452603155087555},
					{'name':'ITS_US_Discord','id':707273522170560513}]

#define the channel we want to read from
selected_channel = channel_details[1]['id']

#define a message limit so we dont get tons of messages that could crash program (from too large a mem allocation in USSL)
message_limit = 15

#clean up heap
gc.collect()

#define a filename for where messages are saved
filename = "gradcap_test"

#add the message details to a text file for later use
def append_text_to_file(message):
	f = open(filename+".txt", 'a')
	f.write("{}|{}|{}|{}".format(message['id'],message['timestamp'],message['name'],message['message']))
	f.close()

#handle getting messages from discord and displaying sprites
def normal_operation():
	global last_message_id
	global last_sprite_index

	#run this routine until REPL cancels routine
	while True:
		#create empty array of stored messages
		stored_messages = []
		#define var to see if we received a message in this loop
		handled_message = False
		#if there was a last message, get data from channel after last message ID
		if last_message_id is not None:
			latest_messages = discbot.get_channel_messages(selected_channel, limit=message_limit, after=last_message_id)
		#otherwise get the last message_limit number of messages
		else:
			latest_messages = discbot.get_channel_messages(selected_channel, limit=message_limit)
		#load the retrieved messages as json objects
		loaded_messages = json.loads(latest_messages)

		#create an iter to move through loaded_messages
		for index in range(len(loaded_messages)):
			#get the loaded message, start from last message (oldest message)
			message = loaded_messages[len(loaded_messages)-index-1]
			#iter through bot_identifier array
			for bot_ident in bot_identifier:
				#if the bot identifier is in the message content
				if bot_ident in message['content']:
					#filter message of bad words and replace bot_identifier with ''
					parsed_message = tfilt.filter_text(message['content'].replace(bot_ident, ''))
					#add the message details to stored_messages
					stored_messages.append({'id': message['id'], 'name':message['author']['username'], 'message':parsed_message[1:], 'timestamp':message['timestamp']})
					#update last_message_id
					last_message_id = message['id']
					#update handled_message var
					handled_message = True

		#print the new messages to REPL
		print("new messages")
		print(stored_messages)
		#iter through stored_messages
		for index in range(len(stored_messages)):
			#get message from array
			message_data = stored_messages.pop()
			#add message details to text file
			append_text_to_file(message_data)
			#format message for gradcap display
			message = '@'+message_data['name']+': '+message_data['message']
			print(message)
			#define a default frame_speed
			speed = 50
			#get number of chars in message (after username)
			message_len = len(message.split(': ')[1])
			#if message length is over threshold, change speed
			if message_len > 15:
				speed = 32
			if message_len > 30:
				speed = 15
			#display the message using speed as frame_speed
			cap.display_7x4_text(message, frame_speed=speed)

		#clean up heap
		gc.collect()
		#check if stored message array is empty (will be true)
		if len(stored_messages) == 0 and handled_message == False:
			#reset index if larger than sprite array len - 1 (ignoring owl sprite)
			if last_sprite_index >= (len(sprites)-1):
				last_sprite_index = 0
			#fisplay sprite for 5 seconds, increment counter index
			cap.display_sprite(sprites[last_sprite_index])
			sleep_ms(5000)
			last_sprite_index += 1

#show TU sprites in succession
def tu_sprites(duration=2000):
	while True:
		cap.display_sprite(sprites[4])
		sleep_ms(duration)
		cap.display_sprite(sprites[5])
		sleep_ms(duration)
		cap.display_sprite(sprites[6])
		sleep_ms(duration)
		cap.display_sprite(sprites[7])
		sleep_ms(duration)

#default main
if __name__ == "__main__":
	#start with normal operation
	normal_operation()
