#!/usr/bin/env python

##ZODB imports
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
#import ZODB.lock_file
import transaction
from AccessControl import ClassSecurityInfo, getSecurityManager
import Globals
from zope.app.component.hooks import getSite
class FilePortalList(object):
    """
    Clase FilePortalList
    """
    security = ClassSecurityInfo()
    instance=None
    def __new__(cls, *args, **kargs):
        """
        Singleton Method for the class
        """
        if cls.instance==None:
            cls.instance = object.__new__(cls, *args, **kargs)
        return cls.instance

    def __init__(self):
	"""
	#TODO: Revisar Puntos de Montaje
	"""
	import pdb; pdb.set_trace()
	self.site=getSite()
        self.waiting=[]
        self.video ={"":""}
        self.current=""
        self.ready=[]
        databasename='cenditelmultimedia.fs'
        storage = FileStorage(databasename)
        db = DB(storage)
        self.connection = db.open()
        self.root = self.connection.root()
        return

    security.declarePublic('CheckItemZODB')
    def CheckItemZODB(self, id):
        try:
            #import pdb; pdb.set_trace()
            self.root[id]
            return True
        except KeyError:
            return False

    security.declarePublic('AddObjectZODB')
    def AddObjectZODB(self, id, elemento):
        """
        Agrega elementos a la ZODB
        """
        self.root[id]=elemento
        return

    security.declarePublic('SaveInZODB')
    def SaveInZODB(self):
        """
        Realiza el guardado en la ZODB
        """
        transaction.commit()
        #self.connection.close()
        return 

    security.declarePublic('RegisterWaitingFile')
    def RegisterWaitingFile(self, idfile='', PathVideo=''):
        """
        Registra un archivo a guardar en la ZODB, el cual se encuentra en espera
        """
        #self.ConectZODB()
        self.video={idfile: PathVideo}
        if self.root['waiting']==None or self.root['waiting']=='' or self.root['waiting']==[]:
            self.root['waiting']=[self.video]
        else:
            TemporalList=self.root['waiting']
            if not self.video in TemporalList:
                TemporalList.append(self.video)
                del(self.root['waiting'])
                self.root['waiting']=TemporalList
                self.SaveInZODB()
                """
                Ver cambio de valor con pdb, ver cuando cambia a None
                """
        return
        
    security.declarePublic('ListOfFileWaiting')
    def ListOfFileWaiting(self):
        """
        Devuelve la lista de archivos en espera en la ZODB
        """
        List=root['waiting']
        
        return List
    
    security.declarePublic('RegisterReadyFile')
    def RegisterReadyFile(self, idfile='', PathVideo=''):
        """
        Registra un archivo que ya esta convertido en la lista correspondiente
        """
        self.video={idfile: PathVideo}
        self.ready=self.root['ready']
        TemporalList=self.ready
        if not self.video in TemporalList:
            TemporalList.append(self.video)
            del(self.root['ready'])
            self.root['ready']=TemporalList
            #self.SaveInZODB()
        return
    
    security.declarePublic('uploaded')
    def uploaded(self, idfile='', PathFile=''):
        """
        Verifica si el archivo guardado ya ha sido cargado previamente
        """
        file={idfile: PathFile}
        self.waiting=self.root['waiting']
        """
        se vuelve NoneType, porque?
        """
        if self.waiting==None:
            return False
        elif file in self.waiting:
            return True
        else:
            return False

    security.declarePublic('available')
    def available(self, idfile='', PathVideo=''):
        #import pdb; pdb.set_trace()
        ###Verificar valores recibidos en available
        file={idfile: PathVideo}
        self.ready=self.root['ready']
        if file in self.ready:
            return True
        else:
            return False

    security.declarePublic('transcoding')
    def transcoding(self, PathVideo=''):
        video=PathVideo
        self.current=self.root['current']
        if video==self.current:
            return True
        else:
            return False

    security.declarePublic('FileWaitings')
    def FileWaitings(self):
        #self.ConectZODB()
        self.waiting=self.root['waiting']
        #self.SaveInZODB()
        #import pdb; pdb.set_trace()
        if self.waiting==None:
            return 0
        else:
            size=len(self.waiting)
        return size

    security.declarePublic('WaitingElement')
    def WaitingElement(self):
        #self.ConectZODB()()
        self.waiting=self.root['waiting']
        element=self.waiting[0]
        print "interrupcion en WaitingElement"
        #import pdb; pdb.set_trace()
        return element

    security.declarePublic('Delete')
    def DeleteElement(self, idfile='', path=''):
        self.waiting=self.root['waiting']
        element=self.waiting[0]
        TemporalList=self.waiting.remove(element)
        del(self.root['waiting'])
        self.root['waiting']=TemporalList
        print "interrupcion en DeletElement"
        #import pdb; pdb.set_trace()
        #self.SaveInZODB()
        return

    security.declarePublic('AddActiveTranscoding')
    def AddActiveTranscoding(self, filerute=''):
        print "Interrupcion en activetranscoding"
        #import pdb;pdb.set_trace()
        if self.root['current']=="":
            self.current=filerute
            self.root['current']=self.current
        else:
            pass
        return
    
    security.declarePublic('CurrentTranscoding')
    def CurrentTranscoding(self):
        current=self.root['current']
        return current

    security.declarePublic('RemoveActiveTranscoding')
    def RemoveActiveTranscoding(self):
        del(self.root['current'])
        self.root['current']=""
        return

    security.declarePublic('AddReadyElement')
    def AddReadyElement(self, idfile='', PathToOriginalFile=''):
        self.ready=self.root['ready']
        del(self.root['ready'])
        video={idfile:PathToOriginalFile}
        self.ready.append(video)
        self.root['ready']=self.ready
        return
#TODO
"""
1) Necesito crear un metodo que va a ser una interfaz de la funcion <len()> para conocer la cantidad de registros
existentes en las listas en la ZODB.

2) Actualizar los script que realizan el registro de la aplicacion y como son guardados los elementos en los archivos para guardar ahora en la ZODB, usar los metodos de 

3) Verificar las estructuras de decision, para ver si realizar las revisiones a nivel del metodo trans__init__ o en los metodos usados por este.

4) Validar el uso de la ZODB de Plone o la creacion de otra adicional unica para el producto

"""
"""
        root[idvideo]=PathVideo
        >>> temp=root['una-lista']
        >>> temp
        ['1', '2', '3', '4']
        >>> temp.append('5')
        >>> del( root['una-lista'])
        >>> root.keys()
        ['otra-lista']
        >>> root['una-lista']=temp
        >>> root['una-lista']
        ['1', '2', '3', '4', '5']
        >>> root.keys()
        ['una-lista', 'otra-lista']
        >>> transaction.commit()


def trans_init_(STORAGE, path, filenamesaved, PARAMETRES_TRANSCODE):#tal ve z haya que pasar folder para el trascode
    #import time
        #folderfile=MFN.DeleteSpaceinNameOfFolderFile(title)
	PathToOriginalFile = STORAGE + path +'/'+ filenamesaved
	newfolderfile=MTD.nginxpath(PathToOriginalFile)
	#print "EL NEW FOLDERFILE EN CONVERT" + newfolderfile
	print "Waiting = "+ str(MTD.uploaded(PathToOriginalFile))
	print "Ready = "+ str(MTD.available(newfolderfile))
	print "Searching file: "+ PathToOriginalFile
	print "Files beafore Transcode "+ str(FAML.NumberOfRegestriesMethod1("waiting.nav"))
	print "uploaded = " + str(MTD.uploaded(PathToOriginalFile)) + "available"+ str(MTD.available(newfolderfile)) + "transcoding =" + str(MTD.transcoding(PathToOriginalFile))
	if MTD.uploaded(PathToOriginalFile)== 0 and MTD.available(newfolderfile)== 0 and MTD.transcoding(PathToOriginalFile)== 0:
		#print "|||COMPARANDO EN CONVERT||||||||"
		FAML.CreateBackupFile("waiting.nav", PathToOriginalFile)
		print "File is Waiting"
	print "File after transcode "+str(FAML.NumberOfRegestriesMethod1("waiting.nav"))
	import threading
	if FAML.NumberOfRegestriesMethod1("current.nav")==0:
		class MyThread(threading.Thread):
			def run(self):
				transcodedaemon(PARAMETRES_TRANSCODE)
		MyThread().start()
	return
"""

Globals.InitializeClass(FilePortalList)