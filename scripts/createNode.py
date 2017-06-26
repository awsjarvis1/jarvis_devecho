#!/usr/bin/env python

import boto3
import os
import sys
import yaml
import time
import getopt, sys
import jenkins
from createNodeLib import jenkinsMethod, ec2Method, nodeMetadata

def usage():
    print "createNode.py:\n    This script is for creation of ec2 instance and add it to jenkins"
    print "(this script is specialy designed to jenkins use)\n"
    print "usage:\n    --help/-h    ->    Display help\n"
    print "    --nodeLabel/-n    ->    Under which Label to want to add node\n"
    print "    --numbere/-c    ->    Number of node that need to be added\n"
    print "    --operation/-o    ->    Operation that need to perform (CREATE|TERMINATE)\n"

def createNode(nodeLabel, count):
    nodeMetadataObject = nodeMetadata(nodeLabel)
    ec2MethodObject = ec2Method(nodeMetadataObject)
    jenkinsMethodObject = jenkinsMethod(nodeMetadataObject)
    for x in range(count):
        ec2MethodObject.createInstance()
        jenkinsMethodObject.addNodeToJenkins()

def terminateNode(nodeLabel):
    nodeMetadataObject = nodeMetadata(nodeLabel)
    ec2MethodObject = ec2Method(nodeMetadataObject)
    jenkinsMethodObject = jenkinsMethod(nodeMetadataObject)
    jenkinsMethodObject.deleteNodeByLabel(nodeLabel)
    ec2MethodObject.terminateDeletedInstance()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hnco", ["help", "nodeLabel=", "number=", "operation="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    nodeLabel = None
    number = None
    operation = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-n", "--nodeLabel"):
            nodeLabel = a
        elif o in ("-c", "--number"):
            number = a
        elif o in ("-o", "--operation"):
            operation = a
        else:
            assert False, "unhandled option"
    #print Help option not specifiled 
    if nodeLabel == None:
        print "Error Node Label not specified"
        usage()
        sys.exit(2)
    elif operation == None:
        print "Error Node number not specified"
        usage()
        sys.exit(2)
    elif number == None and operation == 'CREATE':
        print "Error Node number not specified"
        usage()
        sys.exit(2)
    if operation == 'CREATE':
        createNode(nodeLabel, number)
    elif operation == 'TERMINATE':
        terminateNode(nodeLabel)
    # ...

if __name__ == "__main__":
    main()