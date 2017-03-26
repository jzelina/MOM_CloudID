#!/usr/bin/python

# requirements
import socket
import os

"""
Title: MOM to Cloud-ID
----------------------
Create Cloud-ID directory for each OMM in MOM Web directory.

About:
------
This tool read connected OMMs from the MOM.
For each OMM it checks if a folder in '/opt/SIP-DECT-MOM/web/omm_files/Cloud-ID-' is created.

If not a empty folder will be created.
Such a folder can be used to allow OMM file uploads.
"""

__author__ = "Julian Zelina"
__version__ = "0.1"
__name__ = "MoMCloudID"

# enable debug
debug = True

############################
# function

def echo_debug(text, isdebug):

    if isdebug:
        print(text)

############################
echo_debug("\n\nSTART {0}".format(str(__name__) + " - " + str(__version__)), debug)

# connect to MOM
try:
    echo_debug("Connect to MOM: ", debug)

    # Establish TCP connection
    echo_debug("Establish TCP connection", debug)
    s = socket.create_connection(("127.0.0.1", 18181), 5)
    s.settimeout(5)

    # Receive Welcome Screen
    data = s.recv(1024)
    #print "received data:", data

    # Request OMM list
    MESSAGE = 'mcnf oc\nexit\n'
    s.send(MESSAGE)

    # Receive OMM list
    lines = [];
    mydata = ''
    data = ''

    while True:
        #print "data.rcv"
        data = s.recv(1024)
        #print "rx:", data
        if not data:
            break
        lines.append(data)
        mydata = mydata + data

    #print "received data:", lines

    # data = get_response(s)
    #print data

except:
    echo_debug("ERROR could not connect to MOM, check if momconsole is closed. ", debug)
    exit()

# read OMMs
echo_debug("Search for CloudIDs", debug)
#print mydata
tmp = []
tmp = mydata.split()
for val in tmp:
    if len(val) is 12 and val[1:3] in "001":
        echo_debug(("CloudID found: ", val), debug)
        if os.path.exists('/opt/SIP-DECT-MOM/web/omm_files/Cloud-ID-' + val):
            echo_debug(".. already exist", debug)
        else:
            echo_debug(".. create new folder", debug)
            os.makedirs('/opt/SIP-DECT-MOM/web/omm_files/Cloud-ID-' + val)

# exit
