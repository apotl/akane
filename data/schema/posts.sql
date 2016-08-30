create table if not exists posts (
	id integer primary key autoincrement not null,
	thread_id integer not null,
	resto integer not null,

	no integer unique not null,
	time integer not null,

	capcode text,
	com text,
	country text,
	poster_id text,
	trip text,

	foreign key ( thread_id ) references threads ( id )
);
