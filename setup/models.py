#!/usr/bin/python
"""
populateCUIs.py
by Ted Morin

builds the 'models' table in doiarchives from config.py files

N.B: relies on "new_config_gener.py" files in model directories
"""

from connection_config import *
import MySQLdb as db
import json
import sys
import os
import subprocess

# configuration
cnx = db.connect(host = DEFAULT_HOSTNAME,user=DEFAULT_USERNAME,passwd=DEFAULT_PASSWORD,db=DEFAULT_DATEBASE)

cur2 = cnx.cursor()
# refresh the table
refresh_query = """-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: doiarchive
-- ------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `models`
--

DROP TABLE IF EXISTS `models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `models` (

  `id` int(16) NOT NULL AUTO_INCREMENT, /*id category*/
  `DOI` varchar(255)  COLLATE utf8_unicode_ci NOT NULL,
  `papertitle` varchar(255) NOT NULL,
  `modeltitle` varchar(255) NOT NULL,
  `yearofpub` int(16),
  `authors` TEXT,

  `must` TEXT, /*population category*/
  `mustnot` TEXT,
  `mustCUI` TEXT,
  `mustnotCUI` TEXT,

  `inpname` TEXT, /*input category*/
  `inpdesc` TEXT,
  `inpCUI` TEXT,
  `inpunits` TEXT,
  `inpdatatype` TEXT,
  `upper` TEXT,
  `lower` TEXT,
  `numofinputs` int(8),
  
  `output` varchar(255), /*output category*/
  `outcome` varchar(255),
  `outcometime` varchar(3),
  `outputCUI` varchar(255),
  `outcomeCUI` varchar(255),
  
  `filename` TEXT, /*data category*/
  `filepointer` TEXT,
  `datumname` TEXT,
  `datum` TEXT,
  
  `language` varchar(12), /*model category*/
  `uncompiled` TEXT,
  `compiled` TEXT,
  `dependList` varchar(255),
  `example` TEXT,
  
  `model_category` varchar(255), /*other categories: model_category and predictive ability*/
  `type` varchar(255), 
  `metric` varchar(255), 
  `value` varchar(255), 
  `lcl` varchar(255), 
  `ucl` varchar(255), 
  `config` varchar(255),
  
  `modified` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
/*  `uploaded` DATE DEFAULT CURRENT_DATE,*/
  
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci

"""
cur2.execute(refresh_query)
cur2.close()

cur3 = cnx.cursor()
# build the insert query

#vestiges of earlier script
"""
#!/usr/bin/python
# updateconfigs.py
# by Ted Morin
#
# updates all of the configuration files recursively, merges the sql commands into a single file
# set criteria for "configs" at blue lines
# 
"""

USAGE = 'USAGE: run_scripts_in [DEPTH] [DIRECTORY]'

DEPTH = 2
models_path = os.path.abspath(os.path.join(os.getcwd(),"../models"))
START = models_path
os.chdir(models_path)

"""
# input checks
if len(sys.argv) > 3:                           # too many arguments
    print USAGE
    print "ERROR: too many arguments"
    exit(1)
elif 1 < len(sys.argv):                         # more than one argument
    try :
        DEPTH = int(sys.argv[1])
    except :                                    # non-integer depth
        print USAGE
        print "ERROR: non-integer depth"
        exit(1)
    if len(sys.argv) == 3:
        if os.path.isdir(sys.argv[2]):
            START = sys.argv[2]
        else :                                  # invalid directory
            print USAGE
            print 'ERROR: directory invalid'
"""

# runs scripts and returns the sql query as output
def run_scripts_in(mypath,recurs):
    if recurs == DEPTH: return ""
    text = ""
    count = 0
    #print mypath
    os.chdir(mypath)
    
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    onlyfiles.sort()
    notfiles = [f for f in os.listdir(mypath) if ( not os.path.isfile(os.path.join(mypath, f)) and f[0] != '.' )]
    notfiles.sort()
##############################################################################################################
    for f in onlyfiles:
        if f[:5] == "new_c" and f[-3:] == '.py':        # change this line if lines are changed
            thefile = os.path.join(mypath, f)
            #print(thefile)
            p = subprocess.Popen(['python', thefile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            newtxt, newerr = p.communicate()
            text += newtxt + newerr
            count += 1
    
    for d in notfiles:
        text += run_scripts_in(os.path.join(mypath,d),recurs+1)
    
    #print(count)
    #print
    return(text)

# run the scripts and build query
insert_query = run_scripts_in(START,0)
insert_query += "COMMIT\n"


cur3.execute(insert_query)

# clear result sets (https://github.com/farcepest/MySQLdb1/issues/28)
while cur3.nextset():
    # debugging print:
    print('threw out a result set')
    pass

cur3.close()
cnx.close()

#print insert_query
print "models inserted: " + str( (len(insert_query.split('\n')) - 2)/ 2)

