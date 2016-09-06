def _build_akane_path(rel):
	path = list('/'.join(__file__.split('/')[:-1]+[rel]))
	if path[-1] != '/':
		path.append('/')
	return ''.join(path)

DB_ROOT = _build_akane_path('data/db')
DB_ASSETS = _build_akane_path('data/db/assets')
DB_THUMBS = _build_akane_path('data/db/thumbs')
DB_SCHEMAS = _build_akane_path('data/db/schemas')

def _get_schema(type):
	with open(DB_SCHEMAS + type + '.sql') as schemafile:
		return schemafile.read()

DB_SCHEMA = _get_schema('mysql')

DB_MAIN_NAME = "boardarchives"
DB_USERNAME = 'akane'
DB_PASSWORD = 'hyper04ts'
DB_HOSTNAME = 'localhost'

def build_db_path(db_name):
	return 'mysql+mysqldb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOSTNAME + '/' + DB_MAIN_NAME
	#return "sqlite:////" + DB_ROOT + db_name + ".db"
