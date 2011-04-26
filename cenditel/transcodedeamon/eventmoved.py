#!/usr/bin/env python

#import
#import pdb
from urlparse import urlparse, urljoin, urlsplit
from re import match
from datetime import date
import urllib
from os import path, remove, system, listdir
from time import sleep
from shutil import move
#Importaciones del Producto
from cenditel.transcodedeamon.convert import ServiceList
from cenditel.transcodedeamon.convert import MTD

#Importacion del registro del panel de control cenditel.transcodedeamon

from zope.app.component.hooks import getSite
from iw.fss.config import ZCONFIG
from cenditel.transcodedeamon.utils import findThisProcess, isThisRunning, RemoveSlash, RemoveSlashIfNecesary


def MoveObject(object, evt, STORAGE):
    file_object=object.getField(object.portal_type)
    name_original_file=file_object.getFilename(object)
    original_path=path.join(STORAGE,evt.oldParent._getURL(), object.tpURL())
    extension=MTD.CheckExtension(name_original_file)
    path_of_original_object=path.join(original_path,name_original_file)
    original_trascoded_file=MTD.nginxpath(path_of_original_object)
    destination_path=path.join(STORAGE,evt.newParent._getURL(),object.tpURL())
    moved_object=path.join(destination_path, name_original_file)
    moved_transcode_object=path.join(destination_path,MTD.nginxpath(name_original_file))
    if extension is 'ogg' or extension is 'OGG' or extension is 'ogv' or extension is 'OGV':
        return
    else:
        if ServiceList.root['waiting'] is not None:
            #El elemento esta en lista de espera para ser codificado
            if {object.id:path_of_original_object} in ServiceList.root['waiting']:
                ServiceList.root['waiting'].remove({object.id:path_of_original_object})
                ServiceList.root['waiting'].append({object.id:moved_object})
                ServiceList.SaveInZODB()
        elif ServiceList.root['ready'] is not None:
            if {object.id:original_trascoded_file} in ServiceList.root['ready']:
                #El elemento fue recodificado
                ServiceList.root['ready'].remove({object.id:original_trascoded_file})
                if path.isfile(original_trascoded_file)==True and path.isdir(destination_path)==True:
                    move(original_trascoded_file,destination_path)
                    ServiceList.root['ready'].append({object.id:moved_transcode_object})
                    ServiceList.SaveInZODB()
                else:
                    return
        elif path_of_original_object==ServiceList.root['current'] and isThisRunning('/usr/bin/ffmpeg -i '+path_of_original_object):
            # El elemento esta siendo codificado
            print "El archivo actual esta siendo codificado"
            system('/usr/bin/killall ffmpeg')
            if path.isdir(original_path)==True:
                if path.isfile(original_trascoded_file)==True:
                    sleep(3)
                    remove(trascoded_file)
                    ServiceList.root['ready'].remove({ElementID:original_trascoded_file})
                    ServiceList.root['waiting'].append({object.id:moved_object})
                    ServiceList.root['current']=""
                    ServiceList.SaveInZODB()
                else:
                    return
        else:
            return

def RenameObject(object, evt, STORAGE):
    #pdb.set_trace()
    file_object=object.getField(object.portal_type)
    name_original_file=file_object.getFilename(object)
    original_path=path.join(STORAGE,evt.oldParent._getURL(), evt.oldName)
    extension=MTD.CheckExtension(name_original_file)
    path_of_original_object=path.join(original_path,name_original_file)
    original_trascoded_file=MTD.nginxpath(path_of_original_object)
    if evt.oldParent is evt.newParent:
        destination_path=path.join(STORAGE,evt.oldParent._getURL(),evt.newName)
    else:
        destination_path=path.join(STORAGE,evt.newParent._getURL(),evt.newName)
    moved_object=path.join(destination_path, name_original_file)
    moved_transcode_object=path.join(destination_path,MTD.nginxpath(name_original_file))
    #pdb.set_trace()
    if extension is 'ogg' or extension is 'OGG' or extension is 'ogv' or extension is 'OGV':
        return
    else:
        #pdb.set_trace()
        if ServiceList.root['waiting'] is not None:
            #El elemento esta en lista de espera para ser codificado
            if {evt.oldName:path_of_original_object} in ServiceList.root['waiting']:
                ServiceList.root['waiting'].remove({evt.oldName:path_of_original_object})
                ServiceList.root['waiting'].append({evt.newName:moved_object})
                ServiceList.SaveInZODB()
        elif ServiceList.root['ready'] is not None:
            if {evt.oldName:original_trascoded_file} in ServiceList.root['ready']:
                #El elemento fue recodificado
                ServiceList.root['ready'].remove({evt.oldName:original_trascoded_file})
                if path.isfile(original_trascoded_file)==True and path.isdir(destination_path)==True:
                    move(original_trascoded_file,destination_path)
                    ServiceList.root['ready'].append({evt.newName:moved_transcode_object})
                    ServiceList.SaveInZODB()
                else:
                    return
        elif path_of_original_object==ServiceList.root['current'] and isThisRunning('/usr/bin/ffmpeg -i '+path_of_original_object):
            # El elemento esta siendo codificado
            print "El archivo actual esta siendo codificado"
            system('/usr/bin/killall ffmpeg')
            if path.isdir(original_path)==True:
                if path.isfile(original_trascoded_file)==True:
                    sleep(3)
                    remove(trascoded_file)
                    ServiceList.root['ready'].remove({object.id:original_trascoded_file})
                    ServiceList.root['waiting'].append({object.id:moved_object})
                    ServiceList.root['current']=""
                    ServiceList.SaveInZODB()
                else:
                    return
        else:
            return

def type_custom_moved(object, evt, **kwargs):
    request = getattr(object, 'REQUEST', None)
    try:
        integrity_info=request.link_integrity_info
        if integrity_info.has_key('deleted')==True:
            return
        else:
            pass
    except AttributeError:
        pass
    portal = getSite()
    portal_path = '/'.join(portal.getPhysicalPath())
    STORAGE=ZCONFIG.storagePathForSite(portal)
    #pdb.set_trace()
    if hasattr(evt, 'oldName')==True and hasattr(evt,'newName')==True and evt.oldName is not None:
        if match(object.portal_type+"."+str(date.today())+"."+"[+\d]", evt.oldName):
            return
        else:
            if evt.newName is not evt.oldName:
                RenameObject(object, evt, STORAGE)
    
    if request.has_key('-C')==True and request.has_key('__factory__info__')==True \
    and request.has_key('__ac')==True and request.has_key('fieldname')==False \
    and request.has_key('value')==False:
        return
    
    if request.has_key('-C')==False and request.has_key('__factory__info__')==True \
    and request.has_key('__ac')==True and request.has_key('fieldname')==True \
    and request.has_key('value')==True:
        return
    
    if request.has_key('-C')==False and request.has_key('__factory__info__')==True \
    and request.has_key('__ac')==True and request.has_key('fieldname')==True \
    and request.has_key('value')==True and request.has_key('title')==True \
    and request.has_key('id')==True and request.has_key('form.button.save')==True:
        return
    
    if request.has_key('-C')==True and request.has_key('__factory__info__')==False \
    and request.has_key('__ac')==True and request.has_key('__cp')==True and request.has_key('fieldname')==False\
    and request.has_key('value')==False and request.has_key('title')==False \
    and request.has_key('id')==False and request.has_key('traverse_subpath')==True and request._steps[-1]=='object_paste':
        print 'Objeto Pegado en acciones'
        if evt.oldParent==None:
            #Copy/Paste
            #TODO
            return
        else:
            #Cut/Paste
            #TODO
            MoveObject(object, evt, STORAGE)
    
    if request.has_key('-C')==False and request.has_key('__factory__info__')==False \
    and request.has_key('__ac')==True and request.has_key('__cp')==True and request.has_key('fieldname')==False\
    and request.has_key('value')==False and request.has_key('title')==False \
    and request.has_key('id')==False and request.has_key('traverse_subpath')==True and request._steps[-1]=='folder_paste'\
    and request.has_key('selected_obj_paths')==True:
        print "Objeto Pegado en Contents"
        if evt.oldParent==None:
            #Copy/Paste
            #TODO
            return
        else:
            #Cut/Paste
            MoveObject(object, evt, STORAGE)
    
    if request.has_key('-C')==False and request.has_key('__factory__info__')==False \
    and request.has_key('__ac')==True and request.has_key('__cp')==True and request.has_key('fieldname')==False\
    and request.has_key('value')==False and request.has_key('title')==False \
    and request.has_key('id')==False and request.has_key('traverse_subpath')==True and request._steps[-1]=='folder_paste'\
    and request.has_key('selected_obj_paths')==False and request.has_key('folder_paste'):
        print 'Objeto Pegado en acciones'
        
        pdb.set_trace()
        if evt.oldParent==None:
            #Copy/Paste
            #TODO
            return
        else:
            #Cut/Paste
            MoveObject(object, evt, STORAGE)
    return