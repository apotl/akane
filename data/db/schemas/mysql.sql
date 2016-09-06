drop database boardarchives;
create database boardarchives;
grant all on boardarchives.* to akane@localhost;
use boardarchives;

create table if not exists boards (
	id integer primary key auto_increment not null,
	board_name varchar(12) character set utf8 unique not null,

	frequency integer not null,
	quiet integer not null,
	get_images integer not null,
	enabled integer not null
);
create table if not exists threads (
	id integer primary key auto_increment not null,
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
	semantic_url text character set utf8,
	sub text character set utf8,
	tag text character set utf8,

	foreign key ( board_id ) references boards ( id )
);
create table if not exists posts (
	id integer primary key auto_increment not null,
	thread_id integer not null,
	resto integer not null,

	no integer unique not null,
	time integer not null,

	name text character set utf8,
	capcode text character set utf8,
	com text character set utf8,
	country text character set utf8,
	poster_id text character set utf8,
	trip text character set utf8,

	foreign key ( thread_id ) references threads ( id )
);
create table if not exists images (
	id integer primary key auto_increment not null,
	post_id integer not null,

	filedeleted integer,
	spoiler integer,

	tim integer,
	ext text character set utf8,

	filename text character set utf8,
	fsize integer,
	md5 varchar(26) character set utf8,
	tn_w integer,
	tn_h integer,
	w integer,
	h integer,

	foreign key ( post_id ) references posts ( id )
);
