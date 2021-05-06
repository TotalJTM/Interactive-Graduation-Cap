#class to act as a text filter
#will replace "bad words" within string with replacement
class TextFilter:
	def __init__(self):
		#list of bad words, this sucked to put together but I used a "bad word" dictionary I found on the internet
		self.bad_words = [	{'word': 'anal', 'replacement': ''},
							{'word': 'anus', 'replacement': ''},
							{'word': 'arse ', 'replacement': ''},
							{'word': 'ass', 'replacement': ''},
							{'word': 'ass fuck', 'replacement': ''},
							{'word': 'ass hole', 'replacement': ''},
							{'word': 'assfucker', 'replacement': ''},
							{'word': 'asshole', 'replacement': ''},
							{'word': 'assshole', 'replacement': ''},
							{'word': 'bastard', 'replacement': ''},
							{'word': 'bitch', 'replacement': ''},
							{'word': 'black cock', 'replacement': ''},
							{'word': 'bloody hell', 'replacement': ''},
							{'word': 'boong', 'replacement': ''},
							{'word': 'cock', 'replacement': ''},
							{'word': 'cockfucker', 'replacement': ''},
							{'word': 'cocksuck', 'replacement': ''},
							{'word': 'cocksucker', 'replacement': ''},
							{'word': 'coon', 'replacement': ''},
							{'word': 'coonnass', 'replacement': ''},
							{'word': 'crap', 'replacement': ''},
							{'word': 'cunt', 'replacement': ''},
							{'word': 'cyberfuck', 'replacement': ''},
							{'word': 'damn', 'replacement': ''},
							{'word': 'darn', 'replacement': ''},
							{'word': 'dick', 'replacement': ''},
							{'word': 'dirty', 'replacement': ''},
							{'word': 'douche', 'replacement': ''},
							{'word': 'dummy', 'replacement': ''},
							{'word': 'erect', 'replacement': ''},
							{'word': 'erection', 'replacement': ''},
							{'word': 'erotic', 'replacement': ''},
							{'word': 'escort', 'replacement': ''},
							{'word': 'fag', 'replacement': ''},
							{'word': 'faggot', 'replacement': ''},
							{'word': 'fuck', 'replacement': ''},
							{'word': 'Fuck off', 'replacement': ''},
							{'word': 'fuck you', 'replacement': ''},
							{'word': 'fuckass', 'replacement': ''},
							{'word': 'fuckhole', 'replacement': ''},
							{'word': 'god damn', 'replacement': ''},
							{'word': 'gook', 'replacement': ''},
							{'word': 'hard core', 'replacement': ''},
							{'word': 'hardcore', 'replacement': ''},
							{'word': 'homoerotic', 'replacement': ''},
							{'word': 'hore', 'replacement': ''},
							{'word': 'lesbian', 'replacement': ''},
							{'word': 'lesbians', 'replacement': ''},
							{'word': 'mother fucker', 'replacement': ''},
							{'word': 'motherfuck', 'replacement': ''},
							{'word': 'motherfucker', 'replacement': ''},
							{'word': 'negro', 'replacement': ''},
							{'word': 'nigger', 'replacement': ''},
							{'word': 'orgasim', 'replacement': ''},
							{'word': 'orgasm', 'replacement': ''},
							{'word': 'penis', 'replacement': ''},
							{'word': 'penisfucker', 'replacement': ''},
							{'word': 'piss', 'replacement': ''},
							{'word': 'piss off', 'replacement': ''},
							{'word': 'porn', 'replacement': ''},
							{'word': 'porno', 'replacement': ''},
							{'word': 'pornography', 'replacement': ''},
							{'word': 'pussy', 'replacement': ''},
							{'word': 'retard', 'replacement': ''},
							{'word': 'sadist', 'replacement': ''},
							{'word': 'sex', 'replacement': ''},
							{'word': 'sexy', 'replacement': ''},
							{'word': 'shit', 'replacement': ''},
							{'word': 'slut', 'replacement': ''},
							{'word': 'son of a bitch', 'replacement': ''},
							{'word': 'suck', 'replacement': ''},
							{'word': 'tits', 'replacement': ''},
							{'word': 'viagra', 'replacement': ''},
							{'word': 'whore', 'replacement': ''},
							{'word': 'xxx', 'replacement': ''},]

	#function to filter text from input arg "text"
	def filter_text(self, text):
		#iter through each "bad word" and check for usage in text
		for word in self.bad_words:
			#check if word is in lowercase text
			if word['word'] in text.lower():
				#if there is a replacement, replace the word with the replacement
				if word['replacement'] != '':
					text = text.replace(word['word'], word['replacement'])
				#otherwise replace word with 'X_X'
				else:
					text = text.replace(word['word'], 'X_X')
		#return modified text
		return text
