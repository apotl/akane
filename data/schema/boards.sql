create table if not exists boards (
	id integer primary key autoincrement not null,
	board text unique not null,

	frequency integer not null,
	quiet integer not null,
	get_images integer not null
);
