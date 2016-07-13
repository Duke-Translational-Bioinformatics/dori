#!/bin/bash
#####################################
# dorihub.sh
# by Ted M
#
# setup script for a linode/lamp docker container
# apache2 and mysql must started in docker container (for now)

# update the container to make installation possible
apt-get update -y

## install git and pull to a known directory
#apt-get install -y git
#mkdir /home/dori-master
#cd /home/dori-master
#git init
#git remote add origin https://github.com/doirisks/dori.git
#git pull origin master

# install necessary python (condense to a requirements.txt or .yml or something?)
apt-get install -y python2.7
apt-get install -y python-sql
apt-get install -y python-MySQLdb
apt-get install -y python-numpy

# install R?
#TODO

# start mysql server
service mysql start

# make a small sql command file, run it, and delete it
# maybe do this step with python instead?
#echo "CREATE DATABASE doiarchive ; CREATE USER doirisks@localhost IDENTIFIED BY 'bitnami'; GRANT ALL PRIVILEGES ON doiarchive.* TO 'doirisks'@'localhost'; COMMIT;" > sqlsetup.sql
#mysql -u root -p"Admin2015" < sqlsetup.sql
#rm sqlsetup.sql

# run setup scripts
cd /src/setup
./dockersetup.py
./setup.sh

# this should not be necessary TODO
sleep 1
./CUIs.py
sleep 1
./CUIs.py

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
