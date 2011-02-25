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
	

	security.declarePublic("ngixpath")
	def nginxpath(self, PathToOriginalFile):
		outputogg = self.newname(PathToOriginalFile)
		output = unicodedata.normalize("NFKD", u"%s" % outputogg).encode('ascii', 'ignore').lower().replace(' ', '-')
		return output

	security.declarePublic("transcode")
	def transcode(self, PathToOriginalFile, PARAMETRES_TRANSCODE):
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
		if exten=="avi":
			os.system("ffmpeg -i " + filebash + " " + PARAMETRES_TRANSCODE + " "+ output) ##
		if exten=="mp4":
			os.system("ffmpeg -i "+ filebash + " " + PARAMETRES_TRANSCODE + " "+ output) ##
		if exten=="ogg" :
			pass
		if exten=="ogv":
			os.system("cp " + filebash + " " + output)
		if exten=="mpg":
			os.system("ffmpeg -i "+ filebash + " " + PARAMETRES_TRANSCODE + " " + output)
		#else:
		#os.system("ffmpeg -i "+ filebash + " " + PARAMETRES_TRANSCODE + " " + output)
		if exten=="mp3":
			os.system("ffmpeg -i "+ filebash + " " + PARAMETRES_TRANSCODE + " " + output)
		return output

Globals.InitializeClass(MyTranscodeDeamon)
