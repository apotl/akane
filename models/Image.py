from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

class Image(declarative_base()):
	__tablename__ = 'images'

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	post_id = Column(Integer, nullable=False, ForeignKey("posts.id"))

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
