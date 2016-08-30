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
