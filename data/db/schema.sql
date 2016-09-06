create table if not exists boards (
	id integer primary key autoincrement not null,
	board_name text unique not null,

	frequency integer not null,
	quiet integer not null,
	get_images integer not null,
	enabled integer not null
);
create table if not exists threads (
	id integer primary key autoincrement not null,
	board_id integer not null,

	no integer unique not null,
	
	archived integer,
	bumplimit integer,
	custom_spoiler integer,
	imagelimit integer,
	images integer,
	last_modified integer,
	omitted_images integer,
	omitted_posts integer,
	replies integer,
	semantic_url text,
	sub text,
	tag text,

	foreign key ( board_id ) references boards ( id )
);
create table if not exists posts (
	id integer primary key autoincrement not null,
	thread_id integer not null,
	resto integer not null,

	no integer unique not null,
	time integer not null,

	name text,
	capcode text,
	com text,
	country text,
	poster_id text,
	trip text,

	foreign key ( thread_id ) references threads ( id )
);
create table if not exists images (
	id integer primary key autoincrement not null,
	post_id integer not null,

	filedeleted integer,
	spoiler integer,

	tim integer,
	ext text,

	filename string,
	fsize integer,
	md5 string,
	tn_w integer,
	tn_h integer,
	w integer,
	h integer,

	foreign key ( post_id ) references posts ( id )
);
