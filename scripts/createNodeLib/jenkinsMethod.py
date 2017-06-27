#!/usr/bin/env python

import jenkins
import xml.etree.ElementTree as ET
import sys

class jenkinsMethod:
    '''Represents a jenkinsMethod.'''

    def __init__(self, nodeData):
        self.nodeData = nodeData
        self.server = jenkins.Jenkins(self.nodeData.jenkinsUrl,
            username=self.nodeData.jenkinsUsername,
            password=self.nodeData.jenkinsPassword )

    def overWriteNode(self):
        '''Make changes to Node config file for ssh key strategy'''

        newpattern = '<retryWaitTime>0</retryWaitTime>'+"\n"+'    <sshHostKeyVerificationStrategy class="hudson.plugins.sshslaves.verifiers.NonVerifyingKeyVerificationStrategy"/>'
        oldpattern = '<retryWaitTime>0</retryWaitTime>'
        try:
            config = self.server.get_node_config('node1')
            config = config.replace(oldpattern, newpattern)
            self.server.reconfig_node('node1', config)
        except Exception, e1:
            error1 = "Error1: %s" % str(e1)
            print(error1)
            sys.exit(2)

    def createNode(self):
        '''create node with input parameter'''

        # create node with parameters
        params = {
            'port': '22',
            'username': self.nodeData.vmType,
            'credentialsId': self.nodeData.vmType,
            'host': self.nodeData.DNSIp
        }
        try:
            self.server.create_node(
                self.nodeData.instanceId,
                numExecutors=1,
                nodeDescription='RUN time generated AWS Node for ' + self.nodeData.nodeLabel,
                remoteFS='/home/'+self.nodeData.vmType,
                labels=self.nodeData.nodeLabel,
                exclusive=True,
                launcher=jenkins.LAUNCHER_SSH,
                launcher_params=params)
        except Exception, e1:
            error1 = "Error1: %s" % str(e1)
            print(error1)
            sys.exit(2)

    def deleteNode(self):
        '''delete node'''
        try:
            self.server.delete_node(self.instanceId)
        except Exception, e1:
            error1 = "Error1: %s" % str(e1)
            print(error1)
            sys.exit(2)

    def deleteNodeByLabel(self, nodeLabel):
        '''delete node by Labell name'''
        for r in self.server.get_nodes():
            if r['name'] == 'master':
                continue
            config = self.server.get_node_config(r['name'])
            output = ET.fromstring(config)
            if output.find('label').text == nodeLabel:
                self.instanceId = r['name']
                self.nodeData.setDeletedInstance(r['name'])
                self.deleteNode()

    def addNodeToJenkins(self):
        '''This fuction will create node and enable on jenkins server'''
        self.createNode()
        self.overWriteNode()