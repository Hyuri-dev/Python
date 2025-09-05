import mariadb

cnx = mariadb.connect(
  host = "147.135.104.21",
  port =3306,
  user = "jodomode_jpadmin", # usuario del gestor de bd
  password = "xM0-=fdZvO,8JjnD", # contraseña del gestor de bd
  database = "example" # nombre de la bd
)

# Get a cursor
cur = cnx.cursor()

# Execute a query
cur.execute("SELECT CURDATE()")


# Fetch one result
row = cur.fetchone()
print("Current date is: {0}".format(row[0]))

# Close connection
cnx.close()