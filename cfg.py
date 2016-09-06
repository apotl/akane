def _build_akane_path(rel):
	path = list('/'.join(__file__.split('/')[:-1]+[rel]))
	if path[-1] != '/':
		path.append('/')
	return ''.join(path)

DB_ROOT = _build_akane_path('data/db')
DB_MAIN_NAME = "archiver"
DB_ASSETS = _build_akane_path('data/db/assets')
DB_THUMBS = _build_akane_path('data/db/thumbs')

def _get_schema(filename):
	with open(DB_ROOT + filename) as schemafile:
		return schemafile.read()

DB_SCHEMA = _get_schema('schema.sql')

def build_db_path(db_name):
	return "sqlite:////" + DB_ROOT + db_name + ".db"
