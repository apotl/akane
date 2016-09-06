from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

base = declarative_base()

class Board(base):
	__tablename__ = 'boards'

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	board_name = Column(String, unique=True, nullable=False)

	frequency = Column(Integer, nullable=False)
	quiet = Column(Integer, nullable=False)
	get_images = Column(Integer, nullable=False)
	enabled = Column(Integer, nullable=False)

class Thread(base):
	__tablename__ = 'threads'

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)

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

	def deserialize(self,json_obj):
		for col in json_obj.keys():
			db_col = col
			if col == 'id':
				db_col = 'poster_id'
			setattr(self,db_col,json_obj[col])

class Post(base):
	__tablename__ = 'posts'

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	thread_id = Column(Integer, ForeignKey("threads.id"), nullable=False)
	resto = Column(Integer, nullable=False)

	no = Column(Integer, unique=True, nullable=False)
	time = Column(Integer, nullable=False)

	name = Column(String)
	capcode = Column(String)
	com = Column(String)
	country = Column(String)
	poster_id = Column(String)
	trip = Column(String)

	def deserialize(self,json_obj):
		for col in json_obj.keys():
			db_col = col
			if col == 'id':
				db_col = 'poster_id'
			setattr(self,db_col,json_obj[col])

class Image(base):
	__tablename__ = 'images'

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

	filedeleted = Column(Integer)
	spoiler = Column(Integer)

	tim = Column(String)
	ext = Column(String)

	filename = Column(String)
	fsize = Column(String)
	md5 = Column(String)
	tn_w = Column(String)
	tn_h = Column(String)
	w = Column(String)
	h = Column(String)

