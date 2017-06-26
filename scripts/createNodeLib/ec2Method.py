# /usr/bin/python2.7

import boto.ec2
import sys


class ec2Method:
    '''Represents a ec2 methods'''

    def __init__(self, nodeData):
        self.nodeData = nodeData
        auth = {"aws_access_key_id": "%s"%self.nodeData.awsAccessKeyId,
            "aws_secret_access_key": "%s"%self.nodeData.awsSecretAccessKey}
        try:
            self.ec2 = boto.ec2.connect_to_region(self.nodeData.region, **auth)
        except Exception, e1:
            error1 = "Error1: %s" % str(e1)
            print(error1)
            sys.exit(1)

    def runInstance(self):
        '''This method is to create ec2 instance'''

        try:
            ret = self.ec2.run_instances(self.nodeData.image,key_name=self.nodeData.keyName,
            instance_type=self.nodeData.instanceType)
        except Exception, e2:
            error2 = "Error2: %s" % str(e2)
            print(error2)
            sys.exit(1)
        self.instanceid = ret.instances[0].id

    def getInstanceData(self):
        '''Get Data from running instance'''
        while "%s"%ec2.get_only_instances(self.instanceid)[0].ip_address == 'None' or ec2.get_only_instances(self.instanceid)[0].state_code != 16:
            #wait for system come UP
            time.sleep(1)
        self.nodeData.setInstanceId(self.instanceid)
        self.nodeData.setInstanceUrl(ec2.get_only_instances(self.instanceid)[0].public_dns_name)
        self.nodeData.setInstanceIpaddress(ec2.get_only_instances(self.instanceid)[0].ip_address)
 

    def startInstance(self):
        '''Starting the instance...'''
        # change instance ID appropriately
        try:
             self.ec2.start_instances(instance_ids=self.instanceid)

        except Exception, e2:
            error2 = "Error2: %s" % str(e2)
            print(error2)
            sys.exit(1)

    def terminateInstance(self):
        '''Terminate the instance...'''
        # change instance ID appropriately
        try:
             self.ec2.terminate_instances(instance_ids=self.instanceid)

        except Exception, e2:
            error2 = "Error2: %s" % str(e2)
            print(error2)
            sys.exit(1)

    def stopInstance(self):
        '''Stopping the instance...'''
        try:
             self.ec2.stop_instances(instance_ids=self.instanceid)

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

