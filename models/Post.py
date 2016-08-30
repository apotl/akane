from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

class Post(declarative_base()):
	__tablename__ = 'posts'

	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	thread_id = Column(Integer, nullable=False, ForeignKey("threads.id"))
	resto = Column(Integer, nullable=False)

	no = Column(Integer, unique=True, nullable=False)
	time = Column(Integer, nullable=False)

	capcode = Column(String)
	com = Column(String)
	country = Column(String)
	poster_id = Column(String)
	trip = Column(String)
