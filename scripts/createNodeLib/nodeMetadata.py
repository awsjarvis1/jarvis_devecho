import boto3
import os
import sys
import yaml
import time
import getopt, sys
import jenkins

class NodeMetadata:
    '''Represents any Node Metadata or predefined data.'''
    def __init__(self, vmtype, nodeLable):
        self.region = os.environ.get('EC2REGION')
        self.jenkinsUrl = os.environ.get('JENKINS_URL')
        self.jenkinsUsername = os.environ.get('USERNAME')
        self.jenkinsPassword = os.environ.get('PASSWORD')
        self.awsAccessKeyId = os.environ.get('AWS_ID')
        self.awsSecretAccessKey = os.environ.get('AWS_KEY')
        self.keyName = os.environ.get('KEY_NAME')
        self.instanceType = os.environ.get('INSTANCE_TYPE')
        self.awsSecretAccessKey = os.environ.get('AWS_KEY')
        self.keyName = os.environ.get('KEY_NAME')
        self.vmtype = vmtype
        self.nodeLable = nodeLable

    def setInstanceId(self, instanceId):
        '''set instance Id.'''
        self.instanceId = instanceid

    def setInstanceUrl(self, instanceId):
        '''set instaance url.'''
        self.instanceId = instanceid

    def setInstanceIpaddress(self, instanceId):
        '''set instance ipaddress.'''
        self.instanceId = instanceid

    def setDeletedInstance(self, instanceId):
        '''set deleted instance.'''
        if type(self.deletedNodeList) is list:
            self.deletedNodeList.append(instanceId)
        else:
            self.deletedNodeList = []
            self.deletedNodeList.append(instanceId)