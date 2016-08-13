
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Created by: Eddie Espinal
# Created on: August 6, 2016
# Copyright 2016 - EspinalLab, LLC
# www.4hackrr.com - Online Community For Engineers & Electronics Hobbyist!

from mailchimp3 import MailChimp
import sys
import json
import random
from ConfigParser import SafeConfigParser

class WinnerPicker:

	global subscribers
	global DEBUG
	global client
	global list_id

	parser = SafeConfigParser()
	parser.read('config.ini')

	mailchimp_username = parser.get('mailchimp', 'username')
	mailchimp_apikey = parser.get('mailchimp', 'apikey')
	mailchimp_list_id = parser.get('mailchimp', 'list_id')

	# set this to False to execute the logic of updating the CWINNER field to 1
	DEBUG = 0

	client = MailChimp(mailchimp_username, mailchimp_apikey)
	list_id = mailchimp_list_id

	# returns all members inside the list
	json_data = client.member.all(list_id, count=0, offset=0, fields="members.merge_fields.fname,members.email_address,members.id")
	json_objects = json.dumps(json_data)
	json_dict = json.loads(json_objects)

	# create a new list from returned values
	subscribers = []
	for key in json_dict:
	    for subscriber in json_dict[key]:
	       subscriber_name = subscriber.values()[1]["FNAME"]
	       previous_winner = subscriber.values()[1]["CWINNER"]
	       subscriber_email = subscriber["email_address"]
	       subscriber_id = subscriber["id"]

	       if previous_winner !=1:
	       		subscribers.append((subscriber_id, subscriber_name.title(), subscriber_email))
	       

	if not subscribers:
		sys.exit("Error: No subscribers found.")

	def updateSubscriber(self, subscriber_id):
		if not DEBUG:
			# Update the member and set the contest_winner to 1
			member = client.member.get(list_id, subscriber_id)

			merge_dict = {
			                'merge_fields': {
			                	'CWINNER': '1',
			                }
			             }

			client.member.update(list_id, subscriber_id, merge_dict)


	def pickAWinner(self):
		# pick a random winner from the list
		selectedWinner = random.choice(subscribers)
		subscriber_id = selectedWinner[0]
		recipient_name = selectedWinner[1]
		recipient_email = selectedWinner[2]

		# create the response json object
		json_object = {
			"name": recipient_name,
			"email": recipient_email,
			"subscriber_id": subscriber_id
		}

		return json.dumps(json_object)