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
    output = "createNode.py:\n    This script is for creation of ec2 instance and add it to jenkins"+
        "(this script is specialy designed to jenkins use)\n"+
        "usage:\n    --help/-h    ->    Display help\n"+
        "    --nodeLable/-n    ->    Under which Lable to want to add node\n"+
        "    --numbere/-c    ->    Number of node that need to be added\n"+
        "    --operation/-o    ->    Operation that need to perform (CREATE|TERMINATE)\n"+

def createNode(nodeLable, count):
    nodeMetadataObject = new nodeMetadata(nodeLable)
    ec2MethodObject = new ec2Method(nodeMetadataObject)
    jenkinsMethodObject = new jenkinsMethod(nodeMetadataObject)
    for x in range(count):
        ec2MethodObject.createInstance()
        jenkinsMethodObject.addNodeToJenkins()

def terminateNode(nodeLable):
    nodeMetadataObject = new nodeMetadata(nodeLable)
    ec2MethodObject = new ec2Method(nodeMetadataObject)
    jenkinsMethodObject = new jenkinsMethod(nodeMetadataObject)
    jenkinsMethodObject.deleteNodeByLabel(nodeLable)
    ec2MethodObject.terminateDeletedInstance()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hnco", ["help", "nodeLable=", "number=", ""])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    nodeLable = None
    number = None
    operation = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-n", "--nodeLable"):
            nodeLable = a
        elif o in ("-c", "--number"):
            number = a
        elif o in ("-o", "--operation"):
            number = a
        else:
            assert False, "unhandled option"
    #print Help option not specifiled 
    if nodeLable == None:
        print "Error Node Lable not specified"
        usage()
        sys.exit(2)
    elif operation == None:
        print "Error Node number not specified"
        usage()
        sys.exit(2)
    elif number == None && operation == 'CREATE':
        print "Error Node number not specified"
        usage()
        sys.exit(2)
    if operation == 'CREATE':
        createNode(nodeLable, number)
    elif operation == 'TERMINATE':
        terminateNode(nodeLable)
    # ...

if __name__ == "__main__":
    main()