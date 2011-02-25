from zope.interface import implements
from cenditel.transcodedeamon import mytranscode, manipulatefilename, manageZODBList
#Importando Libreria del Sistema Operativo
import os
from AccessControl import ModuleSecurityInfo, getSecurityManager
import Globals

modulesecurity = ModuleSecurityInfo()
MTD=mytranscode.MyTranscodeDeamon()
MFN=manipulatefilename.ManipulateFileName()

ServiceList=manageZODBList.FilePortalList()

modulesecurity.declarePublic('transcodedaemon')
def transcodedaemon(PARAMETRES_TRANSCODE):
	print "The transcode is activated"
	##############
	#import pdb; pdb.set_trace()
	###############
	while(ServiceList.FileWaitings()>0):
		print "Daemon is runing"
		element=ServiceList.WaitingElement()
		listpath=element.values()
		#import pdb; pdb.set_trace()
		PathToOriginalFile=listpath[0]
		listpath=''
		listpath=element.keys()
		idvideo=listpath[0]
		print "It is the file to transcode: " + str(PathToOriginalFile)
		ServiceList.DeleteElement(idvideo, PathToOriginalFile)
		ServiceList.AddActiveTranscoding(PathToOriginalFile)
		#import pdb;pdb.set_trace()
		PathToTranscodedFile = MTD.transcode(PathToOriginalFile, PARAMETRES_TRANSCODE)
		ServiceList.RemoveActiveTranscoding()
		ServiceList.AddReadyElement(idvideo, PathToTranscodedFile)
		ServiceList.SaveInZODB()
	print "Daemon is waiting for File"
	return


modulesecurity.declarePublic('newtrans_init_')
def newtrans_init_(STORAGE, path, filenamesaved, PARAMETRES_TRANSCODE, idvideo):
	PathToOriginalFile = STORAGE + path +'/'+ filenamesaved
	newfolderfile=MTD.nginxpath(PathToOriginalFile)
	print "EL NEW FOLDERFILE EN CONVERT" + newfolderfile
	#import pdb; pdb.set_trace()
	if ServiceList.CheckItemZODB('waiting')==False:
		ServiceList.AddObjectZODB('waiting',[])
		ServiceList.SaveInZODB()
	if ServiceList.CheckItemZODB('current')==False:
		ServiceList.AddObjectZODB('current','')
		ServiceList.SaveInZODB()
	if ServiceList.CheckItemZODB('ready')==False:
		ServiceList.AddObjectZODB('ready',[])
		ServiceList.SaveInZODB()
	if ServiceList.uploaded(idvideo, PathToOriginalFile)== False and ServiceList.available(idvideo, newfolderfile)== False and ServiceList.transcoding(PathToOriginalFile)== False:
		ServiceList.RegisterWaitingFile(idvideo, PathToOriginalFile)
	import threading
	if ServiceList.CurrentTranscoding()=="":
		class MyThread(threading.Thread):
			def run(self):
				transcodedaemon(PARAMETRES_TRANSCODE)
		MyThread().start()
	return
modulesecurity.apply(globals())

