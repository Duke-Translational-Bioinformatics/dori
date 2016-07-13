#!/bin/bash
#####################################
# dorihub.sh
# by Ted M
#
# setup script for a ubuntu:14.04 docker container
# apache2 and mysql must started in docker container (for now)

# update the container to make installation possible
apt-get update -y
apt-get install -y apache2
apt-get install -y mysql-server
apt-get install -y php5

# install necessary python (condense to a requirements.txt or .yml or something?)
apt-get install -y python2.7
apt-get install -y python-sql
apt-get install -y python-MySQLdb
apt-get install -y python-numpy

# install R?
#TODO

# start mysql server
service mysql start

# run setup scripts
cd /src/setup
./dockersetup.py
./setup.sh

# set interface as the default webpage of the server
cp -r /src/interface /var/www/interface
mkdir /var/www/interface/log
chmod -R 755 /var/www/interface
sed -i "s/example.com\/public_html/interface\/public/g" /etc/apache2/sites-available/example.com.conf
sed -i "s/example.com/interface/g" /etc/apache2/sites-available/example.com.conf
cp /etc/apache2/sites-available/example.com.conf /etc/apache2/sites-available/interface.conf
a2dissite example.com.conf 
rm /etc/apache2/sites-available/example.com.conf 
a2ensite interface.conf
chmod -R 755 /src/interface/

# stop the mysql server
service mysql stop
