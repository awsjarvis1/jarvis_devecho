#!/usr/bin/env python

import os
import sys
import configparser

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
        self.deploy = ['chatui', 'image', 'log']
        self.index = 0
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

    def saveData(self):
        ''' This function will save data to config file'''

        config = configparser.ConfigParser()
        if os.path.isfile('deploy_vm.ini'):
            config.read('deploy_vm.ini')
        config[self.deploy[self.index]] = {}
        config[self.deploy[self.index]]['instanceId'] = self.instanceId
        config[self.deploy[self.index]]['instanceUrl'] = self.instanceUrl
        config[self.deploy[self.index]]['DNSIp'] = self.DNSIp
        with open('deploy_vm.ini', 'w') as configfile:
            config.write(configfile)
        self.index = self.index + 1
