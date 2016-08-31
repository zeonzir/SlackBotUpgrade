from slacker import Slacker
import urllib2
import time
import socket
import warnings
import xml.etree.ElementTree as ET
import argparse, os
from subprocess import Popen, PIPE
import shlex

""" Function to ping and ensure the internet is available """
def internet_on():
    try:
        response=urllib2.urlopen('http://www.google.com',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

""" Function to read custom xml and provide data """
def retData(fileXml):
    try:
        tree = ET.parse(fileXml)
    except:
        print "Could not open file! Check file path."

    # Get root node of the tree
    root = tree.getroot()
    for child in root:
        if child.tag == "apitoken":
            return(child.text)

""" Function to handle command execution and simple responses """
def handleCmd(cmd):
    
    # Split commmand into shell-like format
    args = shlex.split(cmd)
    
    proc = Popen(args, stderr=PIPE, shell=True)
    err = proc.communicate()
    
    if "Waiting for existing lock by process" in err:

        while("Waiting for existing lock by process" in err):
            args = shlex.split('clear; rm -rf /z/madantrg/.theano/compiledir_Linux-3.13--generic-x86_64-with-Ubuntu-14.04-trusty-x86_64-2.7.6-64/lock_dir/')
            proc = Popen(args, stderr=PIPE)
            err = proc.communicate()
    
        args = shlex.split(cmd)
        proc = Popen(args, stderr=PIPE)
        err = proc.communicate()

    exitcode = proc.returncode
    return exitcode

                
""" Core functionality """
# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--command', help='command string (Recommend using single quote)')
args = parser.parse_args()

# Ignore warnings (there are few SSL related ones)
warnings.filterwarnings('ignore')
# Set number of mins for timeout
numMinsTillTimeout = 5
timeout = time.time() + 60*numMinsTillTimeout

# Wait for the PI to connect to the internet
while not internet_on():
    # Sleep for one second
    time.sleep(1)

    # Check timeout
    if time.time() > timeout:
        break

# Connect to slack bot
if internet_on():
    slack = Slacker(retData('custom.xml'))
    
    if not (args.command==None):
        # Execute command
        if (not handleCmd(args.command)):    
            # Send command via slackbot
            slack.chat.post_message('informer','Completed execution of command ' + args.command) 
        else:
            # Send command via slackbot
            slack.chat.post_message('informer','Couldn\'t complete execution of command ' + args.command) 

