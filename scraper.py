import requests
import json
import sqlite3
from random import getrandbits
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Board, Thread, Post, Image
import cfg

class BaseScraper:
	def _build_db_path(self,db_name):
		return "sqlite:////" + cfg.DB_ROOT + db_name + ".db"

class BoardScraper(BaseScraper):
	def __init__(self,board):
		self.board = board
		self.db_path = self._build_db_path(cfg.DB_MAIN_NAME)

		self._engine = create_engine(self._build_db_path(cfg.DB_MAIN_NAME))
		self.Session = sessionmaker(bind=self._engine)

		self.conn = self._engine.connect()
		self.session = self.Session(bind=self.conn)

		query = self.session.query(Board).filter(Board.id == self.board.id, Board.enabled == 1)
		if len(list(query)) != 1:
			raise IndexError("Board record with supplied id not found")

		self.board = query[0]

		board_url = 'https://a.4cdn.org/'+self.board.board_name+'/catalog.json'
		board_json = requests.get(board_url).text
		board_by_page = json.loads(board_json)

		self.board_json_by_thread = []
		for page in board_by_page:
			self.board_json_by_thread += [thread for thread in page["threads"] if thread["resto"] == 0]

		self.thread_scrapers = []

	def initialize_available_thread_scrapers(self):
		for thread_json in self.board_json_by_thread:
			if len(list(self.session.query(Thread).filter(Thread.no == thread_json['no']))) == 0:
				thread = Thread()
				thread.no = thread_json["no"]
				thread.board_id = self.board.id
				self.thread_scrapers += [ThreadScraper(thread)]

	def start(self):
		for thread_scraper in self.thread_scrapers:
			thread_scraper.start()

class ThreadScraper(BaseScraper):
	def __init__(self,thread):
		self.thread = thread

		self._engine = create_engine(self._build_db_path(cfg.DB_MAIN_NAME))
		self.Session = sessionmaker(bind=self._engine)

		self.conn = self._engine.connect()
		self.session = self.Session(bind=self.conn)

	def get_json(self):
		query = self.session.query(Board).filter(Board.id == self.thread.board_id)
		if len(list(query)) != 1:
			raise IndexError("Board record with supplied id not found")

		self.board_name = query[0].board_name

		thread_url = 'https://a.4cdn.org/'+self.board_name+'/thread/'+str(self.thread.no)+'.json'
		thread_json = requests.get(thread_url).text
		self.thread_by_posts = json.loads(thread_json)['posts']

		self.post_scrapers = []
		
		self.columns = [col for col in dir(self.thread) if col[0] != '_']

	def save(self):
		for post_json in self.thread_by_posts:
			if post_json['resto'] == 0:
				if len(list(self.session.query(Thread).filter(Thread.no == post_json['no']))) == 0:
					self.thread.deserialize(post_json)
					self.session.add(self.thread)
					self.session.commit()
				break

	def start(self):
		self.get_json()
		self.save()

class ImageScraper(BaseScraper):
	def __init__(self,image):
		self.image = image

	def start(self):
		pass

class PostScraper(BaseScraper):
	def __init__(self,Post):
		self.post = post

	def start(self):
		pass

