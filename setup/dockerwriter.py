#!/usr/bin/python
"""
dockerwriter.py
by Ted Morin

write docker files for python. To build a docker container of a particular compile a docker file 
USAGE: sudo python dockerwriter.py [OPTIONS]

OPTIONS:
-b, --build                 build all docker files
-t, --test                  build just the first docker file

N.B: run models.py and CUIs.py first!
"""

from connection_config import *
import MySQLdb as db
import json
import sys
import os

# a function to get a file extension
def getFileExtension(filename):
    if filename.find(".") == -1:
        return ""
    else :
        return filename[filename.find("."):]

# populate the target directory with the added files from the current working directory, screens blanks
def populate(added, target):
    current_working_directory = os.getcwd()
    target = os.path.abspath(target)
    for item in added:
        if item != "":
            start = os.path.join(current_working_directory, item)
            #print start
            end = os.path.join(target, item)
            #print end
            if os.path.isdir(start):
                os.system('sudo cp -r "' + start + '" "' + end + '"') 
            else :
                os.system('sudo cp "' + start + '" "' + end + '"') 
            # consider using -l (link) for the cp command
            # this option might speed up the process and save disk space, esp for bigger models
            # how would docker build react?

# dockbuild([id, DOI, language, compiled, uncompiled, dependList, example, config])
# builds the docker container
# must be run from the model's DOI directory after Dockerfile has been built
# requires root privileges to run
def dockbuild(model, dockmodel):
    dockmodel = os.path.abspath(dockmodel)
    # make the docker directory
    if not os.path.isdir(dockmodel):
        os.system("sudo mkdir " + dockmodel)
    # ensure that it is clean
    if os.path.samefile(dockmodel,"/"):                 # some error checking
        print "Tried to build in root!"
        return()
    else :
        os.system("sudo rm -rf "+dockmodel+"/*")        # DANGEROUS LINE
    
    # files which will be included in the container
    added = []
    
    # add the compiled files
    for item in model[3]:
        if item != "":
            added.append(item)
        
    # add the uncompiled files
    for item in model[4]:
        if item != "":
            added.append(item)
            
    # add the dependency list if it exists
    if model[5] != None and model[5] != "":
        added.append(model[5])
        
    # add examples if any
    for example in model[6]:
        if example != "":
            added.append(example)
    
    # add the JSON config file (if it exists)
    if model[7] != None and model[7] != "":
        added.append(model[7])
    
    # populate the folder from which the docker container will be built
    populate(added, dockmodel)
    
    # move in the Dockerfile
    os.system("cp Dockerfile_"+ str(model[0]) + " " + dockmodel + "/Dockerfile")
    
    os.system("sudo docker build -t doirisks/model_" + str(model[0]) + " " + dockmodel)
    
if __name__ == '__main__':
    # connect to mysql server
    cnx = db.connect(host=DEFAULT_HOSTNAME,db = DEFAULT_DATEBASE, user=DEFAULT_USERNAME, passwd=DEFAULT_PASSWORD)
    cur = cnx.cursor()

    # get data on the models
    fetch_query = """SELECT id, DOI, language, compiled, uncompiled, dependList, example, config FROM `models`"""
    cur.execute(fetch_query)

    # save the base, should be the path to ......./dori-master/models
    models_path = os.path.abspath(os.path.join(os.getcwd(),"../models"))

    # iterate through all of the models
    model = cur.fetchone()
    while model != None :
        # convert model to a python list
        model = list(model)
        
        # expand json strings
        model[3] = json.loads(model[3]) # compiled
        model[4] = json.loads(model[4]) # uncompiled
        model[6] = json.loads(model[6]) # example(s)
        
        # set the current working directory to the target DOI
        os.chdir( os.path.join(models_path,model[1].replace('/',':')) )
        
        # text of the Dockerfile (starts with comments)
        text = """######################################################################## Dockerfile to build model """ + str(model[0]) + """
# Based on continuumio/miniconda, produced by dockerwriter.py
#######################################################################

"""
        
        # FROM statement
        text += 'FROM continuumio/miniconda\n'

        # MAINTAINER statement
        text += 'MAINTAINER "DOI RISKS"\n'
        
        # ADD a folder containing all model data added
        text += "ADD ./ model"+str(model[0])+"\n"
        
        # RUN to duplicate the first compiled file to give it a uniform name (will not overwrite)
        if model[3] != None and model[3][0] != "":
            text += "RUN cp -n " + os.path.join("/model"+str(model[0]), model[3][0]) + " /model"+str(model[0])+"/model" + getFileExtension(model[3][0]) + '\n'
        
        # RUN to duplicate the first uncompiled file with a uniform name (will not overwrite)
        if len(model[4]) != 0 and model[4][0] != "":
            text += "RUN cp -n " + os.path.join("/model"+str(model[0]),model[4][0]) + " /model"+str(model[0])+"/model" + getFileExtension(model[4][0]) + '\n'
        
        ###################################################################### Language dependencies 
        # rules for python imports (PART I)
        if model[2][:6] == 'python' or model[2] == 'py':
            # install pip
            text += 'RUN conda install -y pip\n'
            
        # rules for R imports (PART I)
        elif model[2] == 'R' or model[2] == 'r':
            model = cur.fetchone()
            continue # just skips them for now!
        
        # rules for unrecognized languages
        else :
            model = cur.fetchone()
            continue # just skips them for now!
        ###################################################################### for ALL languages
        
        # RUN to install model dependencies
        if model[5] != None and model[5] != "": 
            text += "RUN conda install -y --file /model"+str(model[0])+"/" + model[5] + "\n"
        
        # RUN to setup model conda environment and activate it 
        # TODO: the conda env create cannot read a requirements.txt file
        #if model[5] != None and model[5] != "": 
        #    text += "RUN conda env create "                         # create env
        #    text += "--name model"+str(model[0]) + " "
        #    text += "--file " + os.path.join("model"+str(model[0]), model[5]) + " "
        #    text += "\n"
        #    #text += "RUN source activate model" + str(model[0])     # activate the model
        
        # name and write the Dockerfile
        output_name = 'Dockerfile_' + str(model[0])
        with open( output_name ,'w') as output:
            output.write(text)
            
        # build the docker container (if applicable) and ?print progress
        if ('-b' in sys.argv or '--build' in sys.argv):
            dockbuild(model,"../dockmodel")
            #print "image built for model " + str(model[0]) + "!"
        elif ('-t' in sys.argv or '--test' in sys.argv) and (model[0] == 1):
            dockbuild(model,"../dockmodel")
            #print "Test Complete!\nDockerfile written for model " + str(model[0]) + "!"
        else :
            pass
            #print "Dockerfile written for model " + str(model[0]) + "!"
        
        model = cur.fetchone()
    
    # close the connection
    cnx.close()


