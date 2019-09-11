from urlparse import urlparse, urljoin, urlsplit
import urllib
from os import path, remove, system, listdir, mkdir
from time import sleep
#Importaciones del Producto
from cenditel.transcodedaemon.convert import ServiceList
from cenditel.transcodedaemon.convert import MTD
#Importacion del registro del panel de control cenditel.transcodedaemon
import pdb
from zope.app.component.hooks import getSite
from iw.fss.config import ZCONFIG
from cenditel.transcodedaemon.utils import findThisProcess, isThisRunning, RemoveSlash, RemoveSlashIfNecesary
from shutil import copy

def Custom_CopyObjet(object, evt):
    #TODO
    #pdb.set_trace()
    request=getattr(evt.original, 'REQUEST', None)
    portal = getSite()
    portal_path = '/'.join(portal.getPhysicalPath())
    STORAGE=ZCONFIG.storagePathForSite(portal)
    destination_path=path.join(STORAGE,request['PARENTS'][0]._getURL(),evt.object.tpURL())
    original_path=path.join(STORAGE,evt.original._getURL())
    
    """
    while path.isdir(destination_path)==False:
        if path.isdir(destination_path)==False:
            pass
        else:
    """
    file_object=evt.original.getField(evt.original.portal_type)
    file_name=file_object.getFilename(evt.original)
    path_of_original_object=path.join(original_path, file_name)
    extension=MTD.CheckExtension(file_name)
    copy_object=path.join(destination_path, MTD.nginxpath(file_name))
    #pdb.set_trace()
    if extension is 'ogg' or extension is 'OGG'\
    or extension is 'ogv' or extension is 'OGV':
        return
    else:
        #pdb.set_trace()
        if ServiceList.root['waiting'] is not None:
            #El elemento esta en lista de espera para ser codificado
            if {object.id:path_of_original_object} in ServiceList.root['waiting']:
                ServiceList.root['waiting'].append({object.id:copy_object})
                ServiceList.SaveInZODB()
        #pdb.set_trace()
        elif ServiceList.root['ready'] is not None:
            original_trascoded_file=MTD.nginxpath(path_of_original_object)
            
            if {object.id:original_trascoded_file} in ServiceList.root['ready']:
                #El elemento fue recodificado
                pdb.set_trace()
                if path.isdir(destination_path)==False:
                    mkdir(destination_path)
                    copy(original_trascoded_file,copy_object)
                    ServiceList.root['ready'].append({object.id:copy_object})
                    ServiceList.SaveInZODB()
                else:
                    pdb.set_trace()
                    if path.isfile(original_trascoded_file)==True:
                        copy(original_trascoded_file,copy_object)
                        ServiceList.root['ready'].append({object.id:copy_object})
                        ServiceList.SaveInZODB()
        #pdb.set_trace()
        elif path_of_original_object==ServiceList.root['current'] and isThisRunning('/usr/bin/ffmpeg -i '+path_of_original_object):
            # El elemento esta siendo codificado
            print "El archivo actual esta siendo codificado"
            system('/usr/bin/killall ffmpeg')
            if path.isdir(original_path)==True:
                if path.isfile(original_trascoded_file)==True:
                    sleep(3)
                    remove(trascoded_file)
                    ServiceList.root['ready'].remove({ElementID:original_trascoded_file})
                    ServiceList.root['waiting'].append({object.id:copy_object})
                    ServiceList.root['current']=""
                    ServiceList.SaveInZODB()
        else:
            return
    
