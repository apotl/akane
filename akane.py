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

		board_ids = [id[0] for id in list(self.session.query(models.Board.id))]

		self.board_scrapers = []

		for id in board_ids:
			board = models.Board()
			board.id = id
			self.board_scrapers += [scraper.BoardScraper(board)]

	def start(self):
		for board_scraper in self.board_scrapers:
			board_scraper.initialize_available_thread_scrapers()
			board_scraper.start()


