# -*- coding:ISO-8859-1 -*-

import subprocess               # subprocess.check_output("/bin/ps -aux")

def getAddress(interfaces, value, split, pos):

    for interface in interfaces:
        comand = "ifconfig {} | grep '{}' | cut -d \"{}\" -f{}".format(interface, value, split, pos)
        response = subprocess.getoutput(comand)

        address = response.split(' ')[0]
        if(address != interface+':'):
            return address

# this def is try get address from various interfaces
def tryInterfaces():
    interfaces = ['wlp3s0', 'wlp2s0', 'wlp1s0', 'wlp0s0', 'wlan0', 'wlan1', 'wlan2', 'wlan3', 'enp2s0f1', 'enp1s0f1', 'enp0s0f1', 'enp4s0', 'enp2s0', 'eth0', 'eth1', 'eth2', 'eth3']

    IP = getAddress(interfaces, 'inet addr', ':', '2')
    # in different distr linux, the ifconfig response different
    if(IP == ''):
        IP = getAddress(interfaces, 'inet ', ' ', '10')

    BC = getAddress(interfaces, 'Bcast', ':', '3')
    # so, need try the anouther way
    if(BC == ''):
        BC = getAddress(interfaces, 'broadcast', ' ', '16')

    return IP, BC

def getIP_BC():
    return tryInterfaces()