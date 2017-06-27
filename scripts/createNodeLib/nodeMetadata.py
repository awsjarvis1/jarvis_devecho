#!/usr/bin/env python

import os
import sys

class nodeMetadata:
    '''Represents any Node Metadata or predefined data.'''

    def __init__(self, nodeLabel):
        if os.environ.get('EC2REGION') == 'ohio':
            self.region = 'us-east-2'
        elif os.environ.get('EC2REGION') == 'mumbai':
            self.region = 'ap-south-1'
        self.jenkinsUrl = os.environ.get('JENKINS_URL')
        self.jenkinsUsername = os.environ.get('USERNAME')
        self.jenkinsPassword = os.environ.get('PASSWORD')
        self.awsAccessKeyId = os.environ.get('AWS_ID')
        self.awsSecretAccessKey = os.environ.get('AWS_KEY')
        self.keyName = os.environ.get('KEY_NAME')
        self.instanceType = os.environ.get('INSTANCE_TYPE')
        self.awsSecretAccessKey = os.environ.get('AWS_KEY')
        self.keyName = os.environ.get('KEY_NAME')
        self.nodeLabel = nodeLabel
        self.image = os.environ.get(nodeLabel+'_'+os.environ.get('EC2REGION').upper())
        if nodeLabel == 'BUILD':
            self.vmType = 'centos'
        elif nodeLabel == 'DEPLOY':
            self.vmType = 'ubuntu'

    def setInstanceId(self, instanceId):
        '''set instance Id.'''
        self.instanceId = instanceId

    def setInstanceUrl(self, instanceUrl):
        '''set instaance url.'''
        self.instanceUrl = instanceUrl

    def setInstanceIpaddress(self, DNSIp):
        '''set instance ipaddress.'''
        self.DNSIp = DNSIp

    def setDeletedInstance(self, instanceId):
        '''set deleted instance.'''
        try:
            if type(self.deletedNodeList) is list:
                self.deletedNodeList.append(instanceId)
            else:
                self.deletedNodeList = []
                self.deletedNodeList.append(instanceId)
        except:
            self.deletedNodeList = []
            self.deletedNodeList.append(instanceId)
