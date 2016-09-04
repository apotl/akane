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

	def list_boards(self):
		return list(self.session.query(models.Board).all())

	def add_board(self,board):
		matches = self.session.query(models.Board).filter(models.Board.board_name == board.board_name)
		if len(list(matches)) > 0:
			return False
		self.session.add(board)
		self.session.commit()
		return True
	
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

	def list(self):
		"""Prints a list of boards being archived with set archive options."""
		boards = []
		for board in self._akane.list_boards():
			boards += [{'board_name': board.board_name,
				'frequency': board.frequency,
				'quiet': board.quiet,
				'get_images': board.get_images}]

		print('List of boards Akane will archive:')
		print('\t' + 'Board Name' +
			'\t' + 'Frequency' + 
			'\t' + 'Log requests?' +
			'\t' + 'Images?')
		for board in boards:
			print('\t' + board['board_name'] +
				'\t\t' + str(board['frequency']) + 
				'\t\t' + str(board['quiet']) +
				'\t\t' + str(board['get_images']))

	def add(self):
		"""Adds a board to Akane's database for archiving."""
		board = models.Board()
		while not board.board_name:
			print('What board should Akane archive? Enter the board name, excluding slashes: ', end = '')
			board.board_name = input()
		while not board.frequency or board.frequency < 1:
			print('How frequent should the specified board be archived, in minutes? ', end = '')
			try:
				opt_freq = int(input())
				board.frequency = opt_freq
			except:
				pass
		while 1:
			print('Should all requests made while archiving this board be logged? (y/N) ', end = '')
			quiet_opt = input()
			if quiet_opt.lower() == 'y':
				board.quiet = 1
				break
			elif quiet_opt.lower() == 'n' or quiet_opt == '':
				board.quiet = 0
				break
		while 1:
			print('Should images, if present on posts, be downloaded? (Y/n) ', end = '')
			image_opt = input()
			if image_opt.lower() == 'n':
				board.get_images = 0
				break
			elif image_opt.lower() == 'y' or image_opt == '':
				board.get_images = 1
				break

		print('')
		if not self._akane.add_board(board):
			print('ERROR: Supplied board /'+board.board_name+'/ already exists in the database')
		else:
			print('Board /'+board.board_name+'/ added for archiving.')

	def enable(self):
		"""(Not implemented) Enable archiving on a selected board."""
		pass

	def disable(self):
		"""(Not implemented) Disable archiving a selected board."""
		pass

	def edit(self):
		"""(Not implemented) Edit the archive options of a board."""
		pass
