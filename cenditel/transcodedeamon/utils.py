#!/usr/bin/env python

from os.path import isfile

def RemoveSlash(path):
    reverse=path[::-1]
    newpath=""
    if reverse[0]=='/':
        for x in path[:-1]:
            newpath=newpath+x
        return newpath
    else:
        return path

def RemoveSlashIfNecesary(path):
    if path[0]=='/':
        newpath=''
        for x in path[1:]:
            newpath=newpath+x
        return newpath
    else:
        pass
    
    
def findThisProcess( process_name ):
    """
    Code from ShaChris23 in
    http://stackoverflow.com/questions/38056/how-do-you-check-in-linux-with-python-if-a-process-is-still-running
    """
    ps = subprocess.Popen("ps -eaf | grep "+process_name, shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    return output

# This is the function you can use  
def isThisRunning( process_name ):
    """
    Code from ShaChris23 in
    http://stackoverflow.com/questions/38056/how-do-you-check-in-linux-with-python-if-a-process-is-still-running
    """
    output = findThisProcess( process_name )
    if re.search(process_name, output) is None:
        return False
    else:
        return True

def RemoveSlash(path):
    reverse=path[::-1]
    newpath=""
    if reverse[0]=='/':
        for x in path[:-1]:
            newpath=newpath+x
        return newpath
    else:
        return path

def RemoveSlashIfNecesary(path):
    if path[0]=='/':
        newpath=''
        for x in path[1:]:
            newpath=newpath+x
        return newpath
    else:
        pass
    
def CleanRegistry(ServiceList):
    #import pdb;pdb.set_trace()
    lists=('waiting','ready')
    for list_element in lists:
        for object_list in ServiceList.root[list_element]:
            path_to_object=object_list.values()[0]
            if isfile(path_to_object):
                pass
            else:
                ServiceList.root[list_element].remove(object_list)
    #pdb.set_trace()
    return

