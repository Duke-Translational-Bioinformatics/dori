#!/usr/bin/python
"""
dockersetup.py
by Ted Morin

makes a mysql user on the docker container in preparation for other setup files.
(the python component of dockersetup.sh)
"""
import MySQLdb as sql


cnx = sql.connect(host = 'localhost', user = 'root', passwd = 'Admin2015')
cur = cnx.cursor()



cur.execute("CREATE DATABASE doiarchive")
cur.execute("CREATE USER 'doirisks'@'localhost' IDENTIFIED BY 'bitnami'"
cur.execute("GRANT ALL PRIVILEGES ON doiarchive.* TO 'doirisks'@'localhost'")


cur.close()
cnx.close()
