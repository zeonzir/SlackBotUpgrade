from slacker import Slacker
import urllib2
import time
import socket
import warnings
import xml.etree.ElementTree as ET

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
                
""" Core functionality """
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
    
    # Execute command
    

    # Send command via slackbot
    slack.chat.post_message('informer','Completed execution of command') 

