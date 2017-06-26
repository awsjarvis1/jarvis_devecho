# /usr/bin/python2.7

import boto3
import time
import sys


class ec2Method:
    '''Represents a ec2 methods'''

    def __init__(self, nodeData):
        self.nodeData = nodeData

        try:
            s = boto3.session.Session(profile_name=self.nodeData.region)
            self.ec2 = s.resource('ec2')
        except Exception, e1:
            error1 = "Error1: %s" % str(e1)
            print(error1)
            sys.exit(1)

    def runInstance(self):
        '''This method is to create ec2 instance'''

        try:
            ret = self.ec2.create_instances(ImageId=self.nodeData.image,
                MinCount = 1,
                MaxCount = 1,
                KeyName=self.nodeData.keyName,
                InstanceType=self.nodeData.instanceType)
        except Exception, e2:
            error2 = "Error2: %s" % str(e2)
            print(error2)
            sys.exit(1)
        self.instanceid = ret[0].id

    def getInstanceData(self):
        '''Get Data from running instance'''
        while "%s"%self.ec2.Instance(self.instanceid).public_ip_address == 'None' or self.ec2.Instance(self.instanceid).state['Code'] != 16:
            #wait for system come UP
            time.sleep(2)
        self.nodeData.setInstanceId(self.instanceid)
        self.nodeData.setInstanceUrl(self.ec2.Instance(self.instanceid).public_dns_name)
        self.nodeData.setInstanceIpaddress(self.ec2.Instance(self.instanceid).public_ip_address)
 

    def startInstance(self):
        '''Starting the instance...'''
        # change instance ID appropriately
        try:
             self.ec2.Instance(self.instanceid).start()

        except Exception, e2:
            error2 = "Error2: %s" % str(e2)
            print(error2)
            sys.exit(1)

    def terminateInstance(self):
        '''Terminate the instance...'''
        # change instance ID appropriately
        try:
             self.ec2.Instance(self.instanceid).terminate()

        except Exception, e2:
            error2 = "Error2: %s" % str(e2)
            print(error2)
            sys.exit(1)

    def stopInstance(self):
        '''Stopping the instance...'''
        try:
             self.ec2.Instance(self.instanceid).stop()

        except Exception, e2:
            error2 = "Error2: %s" % str(e2)
            print(error2)
            sys.exit(1)

    def createInstance(self):
        '''Get Data from running instance'''
        #create instance as per requirement
        self.runInstance()
        self.getInstanceData();

    def terminateDeletedInstance(self):
        '''Terminate the instance...'''
        # change instance ID appropriately
        for instanceId in self.nodeData.deletedNodeList:
            self.instanceId = instanceId
            self.terminateInstance()

