# -*- coding:ISO-8859-1 -*-

import subprocess               # subprocess.check_output("/bin/ps -aux")

def getFromIFconfig():
    return subprocess.getoutput('ifconfig')

def findInResponse():
    response = getFromIFconfig()

    indexFirst = 0
    indexNext = 0

    IP = ''
    BROADCAST = ''
    try:
        while(IP == ''):            # this while is stop when find the IP and Broadcas or raise the ValueError
            indexFirst = response.index('\n', indexNext+1)+1
            indexNext = response.index('\n', indexFirst+1)

            IP = findInLine(response[indexFirst:indexNext], True)

        while(BROADCAST == ''):
            BROADCAST = findInLine(response[indexFirst:indexNext], False)

            indexFirst = response.index('\n', indexNext+1)+1
            indexNext = response.index('\n', indexFirst+1)

        return IP, BROADCAST

    except ValueError:
        return '', ''

def findInLine(line, isIP):

    line = line.split(' ')
    if(isIP):
        key = 'inet'
    else:
        key = 'broadcast'

    for pos, word in enumerate(line):
        if(word == key):
            return line[pos+1]

    return ''

def getAddress():
    return findInResponse()