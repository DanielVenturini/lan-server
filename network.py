# -*- coding:ISO-8859-1 -*-

import subprocess               # subprocess.check_output("/bin/ps -aux")

def getAddress(interfaces, value, pos):

    for interface in interfaces:
        comand = "ifconfig {} | grep '{}' | cut -d \":\" -f{}".format(interface, value, pos)
        response = subprocess.getoutput(comand)

        address = response.split(' ')[0]
        if(address != interface+':'):
            return address

# this def is try get address from various interfaces
def tryInterfaces():
    interfaces = ['enp2s0', 'wlp1s0', 'eth0', 'wlan0']

    IP = getAddress(interfaces, 'inet addr', '2')
    BC = getAddress(interfaces, 'Bcast', '3')

    return IP, BC

def getIP_BC():
    return tryInterfaces()