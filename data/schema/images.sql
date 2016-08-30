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
