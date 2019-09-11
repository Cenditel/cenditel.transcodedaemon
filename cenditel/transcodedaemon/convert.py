from zope.interface import implements
from cenditel.transcodedaemon import mytranscode, manipulatefilename, manageZODBList
#Importando Libreria del Sistema Operativo
import os
from AccessControl import ModuleSecurityInfo, getSecurityManager
import Globals

from cenditel.transcodedaemon.utils import CleanRegistry
modulesecurity = ModuleSecurityInfo()
MTD=mytranscode.MyTranscodeDeamon()
MFN=manipulatefilename.ManipulateFileName()

ServiceList=manageZODBList.FilePortalList()

modulesecurity.declarePublic('transcodedaemon')
def transcodedaemon():
	print "The transcode is activated"
	##############
	# import pdb; pdb.set_trace()
	###############
	while(ServiceList.FileWaitings()>0):
		print "Daemon is runing"
		element=ServiceList.WaitingElement()
		listpath=element.values()
		#import pdb; pdb.set_trace()
		PathToOriginalFile=listpath[0]
		listpath=''
		listpath=element.keys()
		idfile=listpath[0]
		print "It is the file to transcode: " + str(PathToOriginalFile)
		# import pdb;pdb.set_trace()
		CleanRegistry(ServiceList)
		if os.path.isfile(PathToOriginalFile):
			ServiceList.DeleteElement(idfile, PathToOriginalFile)
			ServiceList.AddActiveTranscoding(PathToOriginalFile)
			PathToTranscodedFile = MTD.transcode(PathToOriginalFile,
						     ServiceList.root['Video_Parameters'],
						     ServiceList.root['Audio_Parameters'],
						     ServiceList.root['Video_ContentTypes'],
						     ServiceList.root['Audio_ContentTypes'],)
			ServiceList.RemoveActiveTranscoding()
			ServiceList.AddReadyElement(idfile, PathToTranscodedFile)
			ServiceList.SaveInZODB()
		else:
			ServiceList.DeleteElement(idfile, PathToOriginalFile)
			print "NOT FOUND "+ PathToOriginalFile
			ServiceList.SaveInZODB()
	print "Daemon is waiting for File"
	return


modulesecurity.declarePublic('newtrans_init_')
def newtrans_init_(STORAGE, path, filenamesaved,\
		   idfile, VIDEO_PARAMETRES_TRANSCODE,\
		   AUDIO_PARAMETRES_TRANSCODE,\
		   audio_content_types, video_content_types):
	###
	PathToOriginalFile = os.path.join(STORAGE,path,filenamesaved)
	###
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
	if ServiceList.CheckItemZODB('Video_Parameters')==False:
		ServiceList.AddObjectZODB('Video_Parameters', VIDEO_PARAMETRES_TRANSCODE)
		ServiceList.SaveInZODB()
	if ServiceList.CheckItemZODB('Audio_Parameters')==False:
		ServiceList.AddObjectZODB('Audio_Parameters', AUDIO_PARAMETRES_TRANSCODE)
		ServiceList.SaveInZODB()
	
	if ServiceList.CheckItemZODB('Video_ContentTypes')==False:
		ServiceList.AddObjectZODB('Video_ContentTypes', video_content_types)
		ServiceList.SaveInZODB()
	if ServiceList.CheckItemZODB('Audio_ContentTypes')==False:
		ServiceList.AddObjectZODB('Audio_ContentTypes', audio_content_types)
		ServiceList.SaveInZODB()

	if ServiceList.root['Audio_Parameters']!=AUDIO_PARAMETRES_TRANSCODE:
		ServiceList.root['Audio_Parameters']=AUDIO_PARAMETRES_TRANSCODE
		ServiceList.SaveInZODB()
	if ServiceList.root['Video_Parameters']!=VIDEO_PARAMETRES_TRANSCODE:
		ServiceList.root['Video_Parameters']=VIDEO_PARAMETRES_TRANSCODE
		ServiceList.SaveInZODB()

	if ServiceList.root['Video_ContentTypes']!=video_content_types:
		ServiceList.root['Video_ContentTypes']=video_content_types
		ServiceList.SaveInZODB()
	
	if ServiceList.root['Audio_ContentTypes']!=audio_content_types:
		ServiceList.root['Audio_ContentTypes']=audio_content_types
		ServiceList.SaveInZODB()

	if ServiceList.uploaded(idfile, PathToOriginalFile)== False and ServiceList.available(idfile, newfolderfile)== False and ServiceList.transcoding(PathToOriginalFile)== False:
		ServiceList.RegisterWaitingFile(idfile, PathToOriginalFile)
	import threading
	if ServiceList.CurrentTranscoding()=="":
		class MyThread(threading.Thread):
			def run(self):
				transcodedaemon()
		MyThread().start()
	return
modulesecurity.apply(globals())

