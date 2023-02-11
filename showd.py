import MySQLdb
import MySQLdb.cursors

conn = MySQLdb.connect(host="localhost", user="root", passwd="02749", db="fitness")

cursor = conn.cursor()
cursor.execute("SELECT * FROM fitness.member")

for row in cursor.fetchall():
    print(row["password"])

conn.close()