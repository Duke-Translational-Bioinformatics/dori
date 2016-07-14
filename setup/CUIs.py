#!/usr/bin/python
"""
populateCUIs.py
by Ted Morin

builds the 'CUIs' table in the doiarchives from the 'models' table
"""


from connection_config import *
import MySQLdb as db
import json

# function to add a CUI without worrying about repeats
def addCUI(CUI):
    if CUIs.has_key(CUI) == False:
        CUIs[CUI] = {}
        CUIs[CUI]['must'] = []
        CUIs[CUI]['mustnot'] = []
        CUIs[CUI]['input'] = []
        CUIs[CUI]['outcome'] = []
        CUIs[CUI]['output'] = []
        CUIs[CUI]['equivalent'] = []
        CUIs[CUI]['derivable'] = []
        CUIs[CUI]['derivedfrom'] = []
        # values not added: name1, name2, name3, datatype, units, defaultlower, defaultupper

# adds a new name to the CUI if it is not a duplicate name
def addname(CUI,newname):
    if CUI.has_key('name1') == False:
        CUI['name1'] = newname
    elif (CUI.has_key('name2') == False) :
        if (newname != CUI['name1']):
            CUI['name2'] = newname
    elif CUI.has_key('name3') == False :
        if (newname != CUI['name2']) and (newname != CUI['name1']):
            CUI['name3'] = newname

# iterates through a models list of CUIs belonging to a certain group adds them to that group w/ respect to the CUI
def treatgroup(group, groupCUI, groupname, modelID):
    group = json.loads(group)
    groupCUI = json.loads(groupCUI)
    for i in range(len(groupCUI)):
        if groupCUI[i] == "":
            pass
        else :
            addCUI(groupCUI[i])
            addname(CUIs[groupCUI[i]], group[i])
            if CUIs[groupCUI[i]].has_key('datatype'):
                if CUIs[groupCUI[i]]['datatype'] != 'bool':
                    pass
                    #print str(groupCUI[i]) + " " + str(group[i]) + " had a data type other than bool. Investigate."
            CUIs[groupCUI[i]]['datatype'] = 'bool'
            CUIs[groupCUI[i]][groupname].append(int(modelID))

    
# configuration
cnx = db.connect(host = DEFAULT_HOSTNAME,user=DEFAULT_USERNAME,passwd=DEFAULT_PASSWORD,db=DEFAULT_DATEBASE)
cur1 = cnx.cursor()

cur1.execute("SELECT id,must,mustCUI,mustnot,mustnotCUI,outcome,outcomeCUI,output,outputCUI,inpname,inpCUI,inpunits,inpdatatype, lower,upper FROM `models`")
DOI = cur1.fetchone()
CUIs = {}
while DOI is not None:

    # debugging commented out
    #print DOI[0]
    # treats "must"
    treatgroup(DOI[1],DOI[2],'must',DOI[0])
    
    # treats "mustnot"
    treatgroup(DOI[3],DOI[4],'mustnot',DOI[0])
    
    # treats "outcome"
    if DOI[6] == None or DOI[6] == "":
            # debugging commented out
            #print "no outcome"
            pass
    else :
        addCUI(DOI[6])
        addname(CUIs[DOI[6]], DOI[5])
        # debugging commented out
        """
        if CUIs[DOI[6]].has_key('datatype'):
            if CUIs[DOI[6]]['datatype'] != 'bool':
                print str(DOI[6]) + " had a data type other than bool. Investigate."
        """
        CUIs[DOI[6]]['datatype'] = 'bool'
        CUIs[DOI[6]]['outcome'].append(int(DOI[0]))
            
    # treats "output"
    if DOI[8] == None or DOI[8] == "":
            # debugging commented out
            #print "no output"
            pass
    else :
        addCUI(DOI[8])
        addname(CUIs[DOI[8]], DOI[7])
        # debugging commented out
        """
        if CUIs[DOI[8]].has_key('datatype'):
            if CUIs[DOI[8]]['datatype'] != 'float':
                print str(DOI[8]) + " had a data type other than float. Investigate."
        """
        CUIs[DOI[8]]['datatype'] = 'float'
        CUIs[DOI[8]]['output'].append(int(DOI[0]))
    
    # treats inputs (expanded from treat group function)
    group = json.loads(DOI[9])
    groupCUI = json.loads(DOI[10])
    units = json.loads(DOI[11])
    datatypes = json.loads(DOI[12])
    defaultlower = json.loads(DOI[13])
    defaultupper = json.loads(DOI[14])
    groupname = 'input'
    for i in range(len(groupCUI)):
        if groupCUI[i] == "":
            pass
        else :
            addCUI(groupCUI[i])
            addname(CUIs[groupCUI[i]], group[i])
            # datatype
            # debugging commented out
            """
            if CUIs[groupCUI[i]].has_key('datatype'):
                if CUIs[groupCUI[i]]['datatype'] != str(datatypes[i]):
                    print  "%s %s had a data type other than %s. Investigate." % (str(groupCUI[i]), str(group[i]), str(datatypes[i]))
            """
            CUIs[groupCUI[i]]['datatype'] = str(datatypes[i])
            # units
            # debugging commented out
            """
            if CUIs[groupCUI[i]].has_key('units'):
                if CUIs[groupCUI[i]]['units'] != str(units[i]):
                    print "%s %s had units other than %s. Investigate." % (str(groupCUI[i]), str(group[i]), str(units[i]))
                    print "Units were %s" % str(CUIs[groupCUI[i]]['units'])
            """
            CUIs[groupCUI[i]]['units'] = str(units[i])
            
            # default lower (not properly tested)
            if defaultlower[i] == "":
                CUIs[groupCUI[i]]['defaultlower'] = None
            elif CUIs[groupCUI[i]].has_key('defaultlower'):
                if CUIs[groupCUI[i]]['defaultlower'] > defaultlower[i] and CUIs[groupCUI[i]]['defaultlower']!=None:
                    CUIs[groupCUI[i]]['defaultlower'] = defaultlower[i]
            else :
                CUIs[groupCUI[i]]['defaultlower'] = defaultlower[i]
                
            # default upper (not properly tested)
            if defaultupper[i] == "":
                CUIs[groupCUI[i]]['defaultupper'] = None
            elif CUIs[groupCUI[i]].has_key('defaultupper'):
                if CUIs[groupCUI[i]]['defaultupper'] < defaultupper[i] and CUIs[groupCUI[i]]['defaultupper']!=None:
                    CUIs[groupCUI[i]]['defaultupper'] = defaultupper[i]
            else :
                CUIs[groupCUI[i]]['defaultupper'] = defaultupper[i]
            
            # add the id to the group
            CUIs[groupCUI[i]][groupname].append(int(DOI[0]))
    
    # get next DOI
    DOI = cur1.fetchone()
    
    
# clear result sets (https://github.com/farcepest/MySQLdb1/issues/28)
while cur1.nextset():
    # debugging print:
    print('threw out a result set')
    pass
    
# close cursor 1
cur1.close()

# special adjustments 1: age cannot be less than zero
if CUIs.has_key('C0804405'):   
    CUIs['C0804405']['defaultlower'] = 0

# special adjustments 2: Sex CUI (not male-specific)
addCUI('C28421')
        # values not added: name1, name2, name3, datatype, units, defaultlower, defaultupper,
CUIs['C28421']['name1'] = 'Sex'
CUIs['C28421']['name2'] = 'Gender'
CUIs['C28421']['name3'] = 'Sex (m/f)'
CUIs['C28421']['datatype'] = 'bool'
CUIs['C28421']['units'] = 'm/f'
CUIs['C28421']['defaultlower'] = None
CUIs['C28421']['defaultupper'] = None


"""
for CUI in CUIs.keys():
    print 
    print CUI
    for element in CUIs[CUI].keys():
        print element, CUIs[CUI][element]
"""

cur2 = cnx.cursor()
# refresh the table
"""
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
"""
refresh_query_1 = """DROP TABLE IF EXISTS `CUIs`"""
refresh_query_2 = """CREATE TABLE `CUIs` (

  `CUI` varchar(255) NOT NULL,      /*identification*/
  `name1` varchar(255),
  `name2` varchar(255),
  `name3` varchar(255),
  
  `must` TEXT,                      /*relations to models*/ 
  `mustnot` TEXT,
  `input` TEXT,
  `outcome` TEXT,
  `output` TEXT,
  
  `equivalent` TEXT,                /*relations to other CUIs*/
  `derivable` TEXT,
  `derivedfrom` TEXT,

  `units` varchar(255),                     /*program features*/
  `defaultupper` varchar(20),
  `defaultlower` varchar(20),
  `datatype` varchar(12),
  
/*  `uploaded` DATE DEFAULT CURRENT_DATE,*/
  
  PRIMARY KEY (`CUI`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci"""

cur2.execute(refresh_query_1)
cur2.execute(refresh_query_2)
cur2.close()

cur3 = cnx.cursor()
# insert query!
all_columns = [  'CUI',  'name1',  'name2',  'name3',    'must',  'mustnot',  'input',  'outcome',  'output',    'equivalent',  'derivable',  'derivedfrom',  'units',  'defaultupper',  'defaultlower',  'datatype']
json_columns = [
  'must',
  'mustnot',
  'input',
  'outcome',
  'output',
  
  'equivalent',
  'derivable',
  'derivedfrom'
]

insert_query = ""
for CUI in CUIs.keys():
    columns = []    # values which are known for the given cui
    values = []     # values for the given cui
    
    # iterate through all possible columns setting values
    for key in all_columns:
        if CUIs[CUI].has_key(key):
            columns.append(key)
            if (key in json_columns):
                values.append(json.dumps(CUIs[CUI][key]))
            else :
                values.append(CUIs[CUI][key])
        elif key == "CUI":
            columns.append(key)
            values.append(CUI)
    for i in range(len(values)):
        if values[i] == None:
            values[i] = "NULL"
        else : 
            values[i] = "'%s'" % str(values[i])
    sub_query = "INSERT INTO `CUIs` (`" + "`, `".join(columns) + "`) VALUES ( " + ", ".join(values) + " );\n"
    insert_query += sub_query
insert_query += "COMMIT\n"

cur3.execute(insert_query)

cur3.close()
cnx.close()

#print insert_query
print "CUIs inserted: " + str(len(CUIs.keys()))
