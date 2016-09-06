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

		query = self.session.query(Board).filter(Board.id == self.board.id)
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
		self.image_scrapers = []
		
		self.columns = [col for col in dir(self.thread) if col[0] != '_']

	def initialize_available_post_scrapers(self):
		for post_json in self.thread_by_posts:
			if len(list(self.session.query(Post).filter(Post.no == post_json['no']))) == 0:
				post = Post()
				post.deserialize(post_json)
				post.thread_id = self.thread.id
				self.post_scrapers += [PostScraper(post)]

	def initialize_image_scrapers(self):
		for post_json in self.thread_by_posts:
			post = self.session.query(Post).filter(Post.no == post_json['no']).first()
			if len(list(self.session.query(Image).filter(Image.post_id == post.id))) == 0:
				image = Image()
				image.deserialize(post_json)
				if image.tim or image.filedeleted == 1:
					image.post_id = post.id
					self.image_scrapers += [ImageScraper(image)]

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

		self.initialize_available_post_scrapers()
		for post_scraper in self.post_scrapers:
			post_scraper.start()

		board = self.session.query(Board).filter(Board.id == self.thread.board_id).first()
		if board.get_images == 1:
			self.initialize_image_scrapers()
			for image_scraper in self.image_scrapers:
				image_scraper.start()

class PostScraper(BaseScraper):
	def __init__(self,post):
		self.post = post

		self._engine = create_engine(self._build_db_path(cfg.DB_MAIN_NAME))
		self.Session = sessionmaker(bind=self._engine)

		self.conn = self._engine.connect()
		self.session = self.Session(bind=self.conn)

	def save(self):
		self.session.add(self.post)
		self.session.commit()

	def start(self):
		self.save()

class ImageScraper(BaseScraper):
	def __init__(self,image):
		self.image = image

		self._engine = create_engine(self._build_db_path(cfg.DB_MAIN_NAME))
		self.Session = sessionmaker(bind=self._engine)

		self.conn = self._engine.connect()
		self.session = self.Session(bind=self.conn)

	def save(self):
		self.session.add(self.image)
		self.session.commit()

	def download(self):
		post = self.session.query(Post).filter(Post.id == self.image.post_id).first()
		thread = self.session.query(Thread).filter(Thread.id == post.thread_id).first()
		board = self.session.query(Board).filter(Board.id == thread.board_id).first()

		image_url = 'https://i.4cdn.org/'+board.board_name+'/'+str(self.image.tim)+self.image.ext
		image_t_url = 'https://i.4cdn.org/'+board.board_name+'/'+str(self.image.tim)+'s.jpg'

		image_data = requests.get(image_url).content
		image_t_data = requests.get(image_t_url).content

		with open(cfg.DB_ASSETS + str(self.image.tim) + self.image.ext, 'wb') as ifile:
			ifile.write(image_data)
		with open(cfg.DB_THUMBS + str(self.image.tim) + 's.jpg', 'wb') as itfile:
			itfile.write(image_t_data)

	def start(self):
		self.save()
		self.download()
