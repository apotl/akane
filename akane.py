import models
import scraper
import cfg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Akane():
	def __init__(self):
		self.db_path = cfg.build_db_path(cfg.DB_MAIN_NAME)

		self._engine = create_engine(cfg.build_db_path(cfg.DB_MAIN_NAME))
		self.Session = sessionmaker(bind=self._engine)

		self.conn = self._engine.connect()
		self.session = self.Session(bind=self.conn)

		self.board_scrapers = []

	def initialize_board_scrapers(self):
		board_ids = [id[0] for id in list(self.session.query(models.Board.id))]

		for id in board_ids:
			board = models.Board()
			board.id = id
			self.board_scrapers += [scraper.BoardScraper(board)]

	def start(self):
		for board_scraper in self.board_scrapers:
			board_scraper.initialize_available_thread_scrapers()
			board_scraper.start()
	
class Ctl():
	def __init__(self):
		print('Initializing Akane ctl.')
		self._akane = Akane()
		print('Type \'help\' for a list of available commands.')

		self._loopctl = True
		while self._loopctl:
			print(':',end='')
			cmd = input()
			if cmd in [function for function in dir(self) if function[0] != '_']:
				getattr(self,cmd)()
			else:
				print('Unknown command.')

	def help(self):
		"""Prints a list of available ctl commands."""
		print('Available ctl commands:')
		for function in [(function,getattr(self,function).__doc__) for function in dir(self) if function[0] != '_']:
			print('\t' + str(function[0]) + '\t' + str(function[1]))

	def start(self):
		"""Starts the archival daemon."""
		print('Starting the archival daemon.')
		self._akane.initialize_board_scrapers()
		self._akane.start()

	def quit(self):
		"""Quits the Akane ctl."""
		print('Quitting the Akane ctl.')
		self._loopctl = False
