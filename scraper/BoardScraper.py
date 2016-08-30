import requests
import json

class BoardScraper:
	def __init__(self,board):
		self.board_name = board_name

	def prepare_board_json(self):
		board_url = 'https://a.4cdn.org/'+self.board_name+'/threads.json'
		board_json = requests.get(board_url).text
		self.board = json.loads(board_json)

	def start(self):
		pass

