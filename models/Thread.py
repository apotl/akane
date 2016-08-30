from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

class Thread(declarative_base()):
	__tablename__ = 'threads'

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	board_id = Column(Integer, nullable=False, ForeignKey("boards.id"))

	no = Column(Integer, unique=True, nullable=False)

	archived = Column(Integer)
	bumplimit = Column(Integer)
	custom_spoiler = Column(Integer)
	imagelimit = Column(Integer)
	images = Column(Integer)
	last_modified = Column(Integer)
	omitted_images = Column(Integer)
	omitted_posts = Column(Integer)
	replies = Column(Integer)
	semantic_url = Column(String)
	sub = Column(String)
	tag = Column(String)

	frequency = Column(Integer, nullable=False)
	quiet = Column(Integer, nullable=False)
	get_images = Column(Integer, nullable=False)
