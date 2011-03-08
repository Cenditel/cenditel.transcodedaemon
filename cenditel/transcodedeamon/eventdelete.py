#!/usr/bin/env python


#importacion python
from urlparse import urlparse, urljoin, urlsplit
import urllib
from os import path, remove, system, listdir
from time import sleep
#Importaciones del Producto
from cenditel.transcodedeamon.convert import ServiceList
from cenditel.transcodedeamon.convert import MTD
#Importacion del registro del panel de control cenditel.transcodedeamon
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from cenditel.transcodedeamon.interfaces import ITranscodeSetings

from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo
from Acquisition import aq_parent
#Importacion debug
import pdb
import subprocess
import re

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


def RemoveObjectsFromHDD(extension, path_of_dir, path_of_object, trascoded_file, ElementID):
    if extension is "ogg" or extension is "OGG":
        if path.isdir(path_of_dir)==False:
            print "FSS ha movido el archivo"
        else:
            print "Algo esta pasando, tenemos un objeto no deseado"
    elif extension is not "ogg" or extension is not "OGG":
        #if path.isdir(path_of_dir)==True and path.isfile(trascoded_file)==True:
        print "El archivo a borrar existe en este directorio"
        if path.isfile(trascoded_file)==True and ({ElementID:trascoded_file} in ServiceList.root['ready'] \
            or path_of_object is ServiceList.root['current']):
            print "El archivo a borrar es "+ trascoded_file
            print "Esperando... 3seg"
            sleep(3)
            remove(trascoded_file)
            print "Archivo Borrado"
            if {ElementID:trascoded_file} in ServiceList.root['ready']:
                print "VERDADERO"
                #pdb.set_trace()
                try:
                    ServiceList.root['ready'].remove({ElementID:trascoded_file})
                except AttributeError:
                    return
            else:
                print "Archivo Borrado"
                return
            if path_of_object is ServiceList.root['current']:
                ServiceList.root['current']=""
        elif ServiceList.root['waiting'] is not None:
            if {ElementID:trascoded_file} in ServiceList.root['waiting']:
                ServiceList.root['waiting'].remove({ElementID:trascoded_file})
        elif path_of_object==ServiceList.root['current'] and isThisRunning('/usr/bin/ffmpeg -i '+path_of_object):
            print "El archivo actual esta siendo codificado"
            system('/usr/bin/killall ffmpeg')
            if path.isdir(path_of_dir)==True:
                print "El archivo a borrar existe en este directorio"
                if path.isfile(trascoded_file)==True:
                    print "El archivo a borrar es "+ trascoded_file
                    sleep(3)
                    remove(trascoded_file)
                    ServiceList.root['ready'].remove({ElementID:trascoded_file})
                    ServiceList.root['current']=""
                else:
                    return

def type_custom_delete(object, evt):
    request = getattr(object, 'REQUEST', None)
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ITranscodeSetings)
    """
    self.SERVER = self.RemoveSlash(settings.adress_of_streaming_server)
    Probablemente no sea usado
    """
    VIDEO_PARAMETRES_TRANSCODE = settings.ffmpeg_parameters_video_line
    AUDIO_PARAMETRES_TRANSCODE = settings.ffmpeg_parameters_audio_line
    audio_content_types=settings.audio_valid_content_types
    video_content_types=settings.video_valid_content_types
    STORAGE = RemoveSlash(settings.mount_point_fss)
    name_original_file=object._v_fss_props[object.Type()].title
    extension=MTD.CheckExtension(name_original_file)
    folderpath=RemoveSlashIfNecesary(urlparse(object.absolute_url())[2])
    path_of_object=path.join(STORAGE,folderpath,name_original_file)
    path_of_dir=path.join(STORAGE,folderpath)
    extension=MTD.CheckExtension(name_original_file)
    trascoded_file=MTD.nginxpath(path_of_object)
    realDelete = False
    ElementID=object.id
    if request.has_key('form.submitted')==True and request.has_key('REQUEST_METHOD')==True \
    and request.has_key('form.button.Cancel')==False:
        if request['REQUEST_METHOD']=='POST':
            """
            Se ejecuta dos veces
            """
            RemoveObjectsFromHDD(extension, path_of_dir, path_of_object, trascoded_file, ElementID)
    elif request.has_key('form.submitted')==False and request.has_key('form.request')==False \
    and request.has_key('selected_obj_paths')== False and request.has_key('paths')==False and \
    request.has_key('-C')==True:
        return
    if request.has_key('form.submitted')==True and request.has_key('form.button.Cancel')==True:
        print "se cancelo el borrado del elemento"
        return
    if request.has_key('selected_obj_paths')==True and request.has_key('paths')==True:
        pdb.set_trace()
        RemoveObjectsFromHDD(extension, path_of_dir,trascoded_file, ElementID)
        return
    if request.has_key('manage_delObjects')==True and request.has_key('ids'):
        """
        Borrar los archivos de file system storage
        """
        print "Borrado del sitio"
    """
    if self.request.form.has_key('form.button.Cancel'):
            import pdb; pdb.set_trace()
            
            Obtener el id y la url absoluta,
            de convert extraer al metodo newfilename para poder obtener el path
            del archivo transcodificado. Verificar si existe. Si el archivo existe
            pero es igual al nombre del objeto recibido, entonces el archivo no lo
            creo ffmpeg si no que fue precargado en ese formato y no hacemos nada.
            De lo contrario el archivo es creado por ffmpeg y procedemos a borrarlo y
            removerlo de la lista de la lista de archivos transcodificados.
            return request.RESPONSE.redirect('www.google.com') 
            parent=self.context.aq_parent
            absolutepath= self.STORAGE + self.PathOfFile + self.filenamesaved
            idfile=self.context.getId
            first_object={idfile:absolutepath}
            second_object={idfile:self.newfiletranscoded}
            if first_object in ServiceList['waiting']:
                ServiceList['waiting'].remove(first_object)
                parent.manage_delObjects(self.context.getId)
            if second_object in ServiceList['ready']:
                parent.manage_delObjects(self.context.gedId)
                ServiceList['ready'].remove(second_object)
                try:
                    os.remove(self.newfiletranscoded)
                except os.error:
                    print "We have a exception deleting the file %s" % (self.newfiletranscoded, )
            ServiceList.SaveInZODB()
    """
    return