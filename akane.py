import models
import scraper
import cfg
from enums import BoardStatus, BooleanText
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

	def get_board(self,board):
		result = self.session.query(models.Board).filter(models.Board.board_name == board.board_name).first()
		if not result:
			return BoardStatus.BOARD_DOES_NOT_EXIST
		return result

	def list_boards(self):
		return list(self.session.query(models.Board).all())

	def add_board(self,board):
		matches = self.session.query(models.Board).filter(models.Board.board_name == board.board_name)
		if len(list(matches)) > 0:
			return BoardStatus.BOARD_EXISTS
		self.session.add(board)
		self.session.commit()
		return BoardStatus.BOARD_OK

	def enable_board(self,board):
		board_to_enable = self.get_board(board)
		if board_to_enable == BoardStatus.BOARD_DOES_NOT_EXIST:
			return BoardStatus.BOARD_DOES_NOT_EXIST
		if board_to_enable.enabled == 0:
			board_to_enable.enabled = 1
		else:
			return BoardStatus.BOARD_SETTING_UNCHANGED
		self.session.commit()
		return BoardStatus.BOARD_OK

	def disable_board(self,board):
		board_to_disable = self.get_board(board)
		if board_to_disable == BoardStatus.BOARD_DOES_NOT_EXIST:
			return BoardStatus.BOARD_DOES_NOT_EXIST
		if board_to_disable.enabled == 1:
			board_to_disable.enabled = 0
		else:
			return BoardStatus.BOARD_SETTING_UNCHANGED
		self.session.commit()
		return BoardStatus.BOARD_OK

	def update_board(self,board):
		board_to_edit = self.get_board(board)
		if board_to_edit == BoardStatus.BOARD_DOES_NOT_EXIST:
			return BoardStatus.BOARD_DOES_NOT_EXIST
		for col in [col for col in dir(board) if col[0] != '_' and col != 'id' and col != 'metadata']:
			setattr(board_to_edit,col,getattr(board,col))
			#board_to_edit.__dict__[col] = board.__dict__[col]
		self.session.commit()
		return BoardStatus.BOARD_OK
	
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

	def _print_boards(self,boards):
		print('\t' + 'Board Name' +
			'\t' + 'Frequency' + 
			'\t' + 'Log requests?' +
			'\t' + 'Get Images?' + 
			'\t' + 'Enabled?')
		for board in boards:
			print('\t' + board.board_name +
				'\t\t' + str(board.frequency) + 
				'\t\t' + BooleanText[board.quiet] +
				'\t\t' + BooleanText[board.get_images] +
				'\t\t' + BooleanText[board.enabled])
		print('')

	def help(self):
		"""Print a list of available ctl commands."""
		print('Available ctl commands:')
		for function in [(function,getattr(self,function).__doc__) for function in dir(self) if function[0] != '_']:
			print('\t' + str(function[0]) + '\t' + str(function[1]))

	def start(self):
		"""Start the archival daemon."""
		print('Starting the archival daemon.')
		self._akane.initialize_board_scrapers()
		self._akane.start()

	def quit(self):
		"""Quit the Akane ctl."""
		print('Quitting the Akane ctl.')
		self._loopctl = False

	def list(self):
		"""Print a list of boards being archived with set archive options."""
		print('List of boards Akane will archive:')
		self._print_boards(self._akane.list_boards())

	def add(self):
		"""Add a board to Akane's database for archiving."""
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

		board.enabled = 1

		print('')
		status = self._akane.add_board(board)
		if status == BoardStatus.BOARD_EXISTS:
			print('ERROR: Supplied board /'+board.board_name+'/ already exists in the database')
		else:
			print('Board /'+board.board_name+'/ added for archiving.')

	def enable(self):
		"""Enable archiving on a selected board."""
		board = models.Board()
		while not board.board_name:
			print('What board should Akane disable archiving for? Enter the board name, excluding slashes: ', end = '')
			board.board_name = input()

		print('')
		status = self._akane.enable_board(board)
		if status == BoardStatus.BOARD_DOES_NOT_EXIST:
			print('ERROR: Supplied board /'+board.board_name+'/ does not exist in the database')
		elif status == BoardStatus.BOARD_SETTING_UNCHANGED:
			print('ERROR: Supplied board /'+board.board_name+'/ is already enabled in the database')
		else:
			print('Board /'+board.board_name+'/ archiving enabled.')

	def disable(self):
		"""Disable archiving a selected board."""
		board = models.Board()
		while not board.board_name:
			print('What board should Akane disable archiving for? Enter the board name, excluding slashes: ', end = '')
			board.board_name = input()

		print('')
		status = self._akane.disable_board(board)
		if status == BoardStatus.BOARD_DOES_NOT_EXIST:
			print('ERROR: Supplied board /'+board.board_name+'/ does not exist in the database')
		elif status == BoardStatus.BOARD_SETTING_UNCHANGED:
			print('ERROR: Supplied board /'+board.board_name+'/ is already disabled in the database')
		else:
			print('Board /'+board.board_name+'/ archiving disabled.')

	def update(self):
		"""Update the archive options of a board."""
		board = models.Board()
		while not board.board_name:
			print('What board should Akane archive? Enter the board name, excluding slashes: ', end = '')
			board.board_name = input()

		current_board = self._akane.get_board(board)
		if current_board == BoardStatus.BOARD_DOES_NOT_EXIST:
			print('ERROR: Supplied board /'+board.board_name+'/ does not exist in the database')
			return

		while not board.frequency or board.frequency < 1:
			print('How frequent should the specified board be archived, in minutes? (current: '+str(current_board.frequency)+') ', end = '')
			try:
				opt_freq = int(input())
				board.frequency = opt_freq
			except:
				pass
		while 1:
			print('Should all requests made while archiving this board be logged? (y/N) (current: '+BooleanText[current_board.quiet]+') ', end = '')
			quiet_opt = input()
			if quiet_opt.lower() == 'y':
				board.quiet = 1
				break
			elif quiet_opt.lower() == 'n' or quiet_opt == '':
				board.quiet = 0
				break
		while 1:
			print('Should images, if present on posts, be downloaded? (Y/n) (current: '+BooleanText[current_board.get_images]+') ', end = '')
			image_opt = input()
			if image_opt.lower() == 'n':
				board.get_images = 0
				break
			elif image_opt.lower() == 'y' or image_opt == '':
				board.get_images = 1
				break

		board.enabled = current_board.enabled

		print('Current board settings:')
		self._print_boards([current_board])
		print('New board settings:')
		self._print_boards([board])
		while 1:
			print('Are these settings ok? (y/N) ', end = '')
			quiet_opt = input()
			if quiet_opt.lower() == 'y':
				status = self._akane.update_board(board)
				if status == BoardStatus.BOARD_DOES_NOT_EXIST:
					print('ERROR: Supplied board /'+board.board_name+'/ does not exist in the database')
				else:
					print('Settings for board /'+board.board_name+'/ updated.')
				break
			elif quiet_opt.lower() == 'n' or quiet_opt == '':
				print('No settings updated for board /'+board.board_name+'/.')
				break

