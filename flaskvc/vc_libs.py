#!/usr/bin/env python
"""
Python program for flat text listing the VMs on an
ESX / vCenter, host one per line.

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
from __future__ import print_function
import atexit
import getpass

from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
#from tools import cli

MAX_DEPTH = 10


def printvminfo(vm, vmarray, depth=1):
    """
    Print information for a particular virtual machine or recurse into a folder
    with depth protection
    """

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > MAX_DEPTH:
            return
        vmlist = vm.childEntity
        for child in vmlist:
            printvminfo(child, vmarray, depth+1)
        return

    summary = vm.summary
    #print(summary.config.name)
    vmarray.append(summary.config.name)

def get_all_vms(si):
    '''
    Function responsible for retrieving VM info
    Input: service_instance pyvmomi connection object
    Output: a dictionary with two values:
        vms_as_string - comma separated string with list of VMs
        vms_as_list - a list with vm names as elements
    - Note: in the future we will add ability to retrieve properties
    '''
    content = si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder
            vmlist = vmfolder.childEntity
            vmarray = []
            for vm in vmlist:
                printvminfo(vm, vmarray)

    # below section - take a list and turn into a string
    vmstring = ""
    for onevm in vmarray:
        if vmstring:
            vmstring = vmstring + ", " + onevm
        else:
            vmstring += onevm

    vm_return = {}
    vm_return['vms_as_string'] = vmstring
    vm_return['vms_as_list'] = vmarray

    return vm_return

def connect(args, config_dict, sec_dict):
    """
    Simple command-line program for listing the virtual machines on a host.
    """
    host = sec_dict.get('vc_config', {}).get('vc_hostname', args.host)
    user = sec_dict.get('vc_config', {}).get('vc_username', args.user)
    pwd = sec_dict.get('secs', {}).get('vc_pass', args.password)
    if not pwd:
        pwdprompt = "Password for "+args.user+"\n"
        pwd = getpass.getpass(prompt=pwdprompt)

    si = None
    try:
        si = SmartConnectNoSSL(host=host,
                               user=user,
                               pwd=pwd,
                               port=443) #int(args.port))
        atexit.register(Disconnect, si)
    except AttributeError:
        raise SystemExit("Must specify host, user and pwd")
        return

    except vim.fault.InvalidLogin:
        raise SystemExit("Unable to connect to host "
                         "with supplied credentials.")
        return
    return si
