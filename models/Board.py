from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

class Board(declarative_base()):
	__tablename__ = 'boards'

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	board = Column(String, unique=True, nullable=False)

	frequency = Column(Integer, nullable=False)
	quiet = Column(Integer, nullable=False)
	get_images = Column(Integer, nullable=False)
