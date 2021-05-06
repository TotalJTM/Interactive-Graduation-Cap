import requests
import ujson as json

#class to handle the discord bot functionality
class MP_DiscordBot:
	#class takes a discord bot token as an arg
	def __init__(self, discord_token):
		self.bot_token = 'Bot ' + discord_token				#format bot token correctly
		self.api_endpoint = 'https://discord.com/api/v9'	#default V9 API

	#function to generate message header (needed to get authorization token)
	def get_header(self):
		return {'Authorization':self.bot_token}

	#function to get messages from a channel
	#takes a channel id (string id for channel), a limit (to limit number of messages in resposne), and after (to get messages after a certain message id)
	def get_channel_messages(self, channel_id, after=None, limit=None):
		#get header data
		header = self.get_header()
		#create an empty query string
		query_string = ''

		#if there is data in after or limit, append that data into query string
		if after is not None:
			query_string += 'after='+str(after)+'&'
		if limit is not None:
			query_string += 'limit='+str(limit)+'&'
		#if query string was modified, add a '?' to start of query string
		if query_string is not '':
			query_string = '?'+query_string

		#create target url from cahnnel id and query string
		target_url = self.api_endpoint+'/channels/'+str(channel_id)+'/messages'+query_string
		#print(target_url)

		#make a request using requests library
		resp = requests.request('GET', target_url, headers=header)
		#print(resp.content)
		#if successful response, return response text
		if resp.status_code == 200:
			return resp.text
		#otherwise display "failed message" and return None
		else:
			print("Failed get messages")
			return None

	