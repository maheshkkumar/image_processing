import MySQLdb

def database():
  connection = MySQLdb.connect(host="localhost", user = "root", passwd = "root", db = "lifelog")
  con = connection.cursor()
  return con, connection


def insert(n, d, lat, lon):
	print "Connecting to Database"
	connection, con = database()
	query = """ INSERT INTO visual(name, description, latitude, longitude) VALUES(n, d, lat, lon)"""
	sql = """INSERT INTO visual(name, description, latitude, longitude) VALUES(%s, %s, %s, %s)""", (n, d, lat, lon)
	con.execute(sql)
	connection.commit()
	return True