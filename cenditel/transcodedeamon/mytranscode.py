##bind context=context
# -*- coding: UTF-8 -*-

#Zope Imports
from AccessControl import ClassSecurityInfo, getSecurityManager
from zope.interface import implements
from Acquisition import aq_inner
from zope.component import getMultiAdapter
import Globals

#Python imports
import os
import unicodedata
import subprocess
#
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

#Importando Libreria del Sistema Operativo
from cenditel.transcodedeamon import findandmanipulateline

class MyTranscodeDeamon:
	"""
	TranscodeDeamon
	"""
	security = ClassSecurityInfo()
	security.declarePublic("__init__")
	def __init__(self):
		"""
		Metodo __init__.py
		"""
		return 

	security.declarePublic('newname')
	def newname(self, video):
		newnamevideo=""
		i=len(video)-1
		while video[i:i+1]!="." and i>0:
			i=i-1
		i=i-1
		if i>=0:
			while i>=0:
				#print "entramos al segundo while"
				newnamevideo=video[i:i+1]+newnamevideo
				i=i-1
		else:
			newnamevideo="_"
		newnamevideo=newnamevideo+".ogg"
		return newnamevideo

	security.declarePublic('bashname')
	def bashname(self, video):
		newbashnamevideo = ""
		for x in video:
			if x==" ":
				x="\ "
			newbashnamevideo = newbashnamevideo+x
		return newbashnamevideo
	
	security.declarePublic("CheckExtension")
	def CheckExtension(self, PathToOriginalFile):
		exten=""
		i=len(PathToOriginalFile)-1
		while PathToOriginalFile[i:i+1]!=".":
			exten=PathToOriginalFile[i:i+1]+exten
			i=i-1
		return exten

	security.declarePublic("ngixpath")
	def nginxpath(self, PathToOriginalFile):
		outputogg = self.newname(PathToOriginalFile)
		output = unicodedata.normalize("NFKD", u"%s" % outputogg).encode('ascii', 'ignore').lower().replace(' ', '-')
		return output

	security.declarePublic("transcode")
	def transcode(self, PathToOriginalFile, VIDEO_PARAMETRES_TRANSCODE,\
		      AUDIO_PARAMETRES_TRANSCODE, audio_content_types,\
		      video_content_types):
		#TODO Number one
		#Por hacer numero uno
		import os
		filebash = self.bashname(PathToOriginalFile)
		output = self.nginxpath(PathToOriginalFile)
		exten=""
		i=len(PathToOriginalFile)-1
		while PathToOriginalFile[i:i+1]!=".":
			exten=PathToOriginalFile[i:i+1]+exten
			i=i-1
		mime = subprocess.Popen("/usr/bin/env file -i "+ filebash, shell=True, \
					stdout=subprocess.PIPE).communicate()[0]
		mimetype=mime.split(":")[1].split(";")[0].replace(" ","")
		del(mime)
		if mimetype in video_content_types:
			#TODO usar aqui stdout como con file 
			os.system("ffmpeg -i " + filebash + " " + VIDEO_PARAMETRES_TRANSCODE + " "+ output)
		elif mimetype in audio_content_types:
			os.system("ffmpeg -i "+ filebash + " " + AUDIO_PARAMETRES_TRANSCODE + " " + output)
		return output

Globals.InitializeClass(MyTranscodeDeamon)
