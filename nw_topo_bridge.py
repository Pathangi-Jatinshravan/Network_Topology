"""
   Copyright 2015 Jatinshravan

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from abc import ABCMeta, abstractmethod

import subprocess

class Bridge(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, name):
        pass

    @abstractmethod
    def add_bridge(self):
        pass
    
    @abstractmethod
    def del_bridge(self):
        pass

class EsxiBridge(Bridge):
    def __init__(self, name):
        self.name = name

    def add_bridge(self):
        subprocess.call(['esxcli', 'network', 'vswitch', 'standard',\
                         'add', '--vswitch-name='+self.name])
        subprocess.call(['esxcli', 'network','vswitch','standard','policy',\
                         'security', 'set', '--allow-promiscuous', 'true', \
                          '--allow-mac-change', 'true', \
                          '--vswitch-name='+self.name])
        subprocess.call(['esxcli', 'network','vswitch','standard','portgroup',\
                         'add', '--portgroup-name='+self.name, \
                          '--vswitch-name='+self.name])

    def del_bridge(self):
        subprocess.call(['esxcli', 'network','vswitch','standard','portgroup',\
                         'remove', '--portgroup-name='+self.name, \
                          '--vswitch-name='+self.name])
        subprocess.call(['esxcli', 'network', 'vswitch', 'standard',\
                         'remove', '--vswitch-name='+self.name])

class LinuxBridge(Bridge):
    def __init__(self, name):
        self.name = name

    def add_bridge(self):
        subprocess.call(['brctl', 'addbr', self.name])
        subprocess.call(['ip', 'link', 'set', self.name, 'up']) 

    def del_bridge(self):
        subprocess.call(['ip', 'link', 'set', self.name, 'down']) 
        subprocess.call(['brctl', 'delbr', self.name])

class OVSBridge(Bridge):
    def __init__(self, name):
        self.name = name

    def add_bridge(self):
        subprocess.call(['ovs-vsctl', 'add-br', self.name])
        subprocess.call(['ip', 'link', 'set', self.name, 'up']) 

    def del_bridge(self):
        subprocess.call(['ip', 'link', 'set', self.name, 'down']) 
        subprocess.call(['ovs-vsctl', 'del-br', self.name])
