"""
pythonrisk.py
by Ted Morin

Handler for python risk requests

Expects: a repository directory, a model's DOI, its filename, and the model's arguments
Output: a single risk score or "error[: error text]" on failure

ARGUMENT FORMAT:
accepts only floats and integers
floats must have a decimal point
integers must NOT have a decimal point
"""

# import the imports
import os
import sys
import imp
import string

def error(text = ""):
    if text == "":
        print "error"
        exit(1)
    else :
        print "error: " + text
        exit(1)

# unpack arguments
repopath = sys.argv[1]
modelDOI = string.replace(sys.argv[2],'/',':')
modelname = sys.argv[3]
arguments = sys.argv[4:]
modelfile = os.path.join(os.path.join(repopath,modelDOI), modelname)

# check path and model
if not os.path.exists(modelfile):
    error("model does not exist")
if os.path.isdir(modelfile) or modelfile[-3:] != ".py":
    error("model labeled incorrectly")

# change all arguments to integers or floats
for i in range(len(arguments)):
    if arguments[i].find('.') == -1 :       # has no decimal point: integer/bool
        arguments[i] = int(arguments[i])
    else :
        arguments[i] = float(arguments[i])  # has decimal point: float

# import the model
m = imp.load_source(modelname[:-3], modelfile[:-3], open(modelfile, 'r') )

# try to print the output
try :
    print m.model(*arguments)
except :
    error("error with function")
