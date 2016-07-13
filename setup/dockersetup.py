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
cur.execute("CREATE USER 'doirisks'@'localhost' IDENTIFIED BY 'bitnami'")
cur.execute("GRANT ALL PRIVILEGES ON doiarchive.* TO 'doirisks'@'localhost'")

# clear result sets (https://github.com/farcepest/MySQLdb1/issues/28)
while cur.nextset():
    # debugging print:
    print('threw out a result set')
    pass


cur.close()
cnx.close()
