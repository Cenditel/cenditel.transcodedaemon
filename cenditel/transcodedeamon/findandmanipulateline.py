####Este es un script de prueba para pasar la seguridad de Zope####
##bind context=context
# -*. coding ut8
from AccessControl import ClassSecurityInfo, getSecurityManager
import Globals

from zope.interface import implements
from Acquisition import aq_inner
from zope.component import getMultiAdapter



#Importando Libreria del Sistema Operativo
import os

class FindAndManipulateLine:
	security = ClassSecurityInfo()
	security.declarePublic("__init__")
	def __init__(self):
		return
	
	security.declarePublic("LoadFileAndRead")
	def LoadFileAndRead(self, name):
		#antiguo loadfile
		#TODO Number 2
		"""
		This method read the information in a file and make a list whit that, \n
		then find the specific line request to the ubication of the file
		"""
		FileObject=open(name,'r')
		cadena=''
		AllLines=FileObject.readlines()
		FileObject.close()
		for line in AllLines:
		    cadena=cadena+line
		return cadena

	security.declarePublic("NumberOfRegestriesMethod2")
	def NumberOfRegestriesMethod2(self, name):
		#antiguo numreg2
		#TODO Number 2
		"""
		This method read and find the number of regestries in a file
		"""
		enters=0
		contents=self.LoadFileAndRead(name)
		for c in contents:
		  d=str(ord(c))
		if c=="\n":
			enters=enters+1
		output=enters-1
		return output


	security.declarePublic("NumberOfRegestriesMethod1")
	def NumberOfRegestriesMethod1(self,name):
		"""
		This method read and find the number of regestries in a file
		"""
		#antiguo numreg
		#TODO Number 2
		f=open(name,"r")	
		contents=f.readlines()
		n=0
		for linea in contents:
		    n=n+1
		return n-2

	security.declarePublic("CreateFilesBoxForConvert")
	def CreateFilesBoxForConvert(self):
		#antiguo create box        
		"""
		This method create all files need it for the use of the Convert program
		"""
		#TODO Number 2
		available=open("waiting.nav",'w')
		available.write("\n")
		available.close()
		available=open("current.nav",'w')
		available.write("\n")
		available.close()
		available=open("ready.nav",'w')
		available.write("\n")
		available.close()
		pass

	security.declarePublic("CreateBackupFile")
	def CreateBackupFile(self, name, item):
		#antiguo register
		"""
		This method create a configuration file to manage the data in secure way \n 
		copy and paste a file in a new file for backup
		"""
		#TODO Number 2
		contents=self.LoadFileAndRead(name)
		dfile=open('respaldo.bak',"w")
		dfile.write(contents)
		dfile.close()
		dfile=open(name,"w") 
		dfile.write("\n"+item+contents) 
		dfile.close()


	security.declarePublic("delete")
	def delete(self, name):
	     #print str(self.NumberOfRegestriesMethod1(name)-1)
	     #TODO Number 2
	     self.delete2(name, self.NumberOfRegestriesMethod1(name)-1)
	     
	

	security.declarePublic("delete2")
	def delete2(self, name, item):
		"""
		ThisMethod delete files from the backup file and then from the original file \n
		it is call it by the delete method
		"""
		#TODO Number 2
		count=0
		dfile=open(name,"r")
		contents=self.LoadFileAndRead(name)
		dfile.close()
		dfile=open('respaldo.bak',"w")
		dfile.write(contents)
		dfile.close()
		dfile1=open("respaldo.bak","r")
		dfile2=open(name,"w")
		dfile2.write("\n")
		c=dfile1.read(1)
		c=dfile1.read(1)
		enters=0
		while enters < self.NumberOfRegestriesMethod1("respaldo.bak")-1:
			nombre=""
			while c!="\n":
				nombre=nombre+c
				c=dfile1.read(1)
			enters=enters+1
			c=dfile1.read(1) 
			if nombre!=item:
				dfile2.write(nombre+"\n")
		dfile2.write("\n")
		dfile2.close()
		dfile1.close()


	security.declarePublic("DeleteElementFromList")
	def DeleteElementFromList(self, name, item):
		#antiguo delete3
		#TODO Number 2
		"""
		This method delete elements from the list in the config files using /n
		a backup file to work
		"""
		count=0
		dfile=open(name,"r")
		contents=self.LoadFileAndRead(name)
		dfile.close()
		dfile=open('respaldo.bak',"w")
		dfile.write(contents)
		dfile.close()
		dfile1=open("respaldo.bak","r")
		dfile2=open(name,"w")
		dfile2.write("\n")
		c=dfile1.read(1)
		c=dfile1.read(1)
		for x in (1,self.NumberOfRegestriesMethod1("respaldo.bak")):
			nombre=""
		while c!="\n":
			nombre=nombre+c
			c=dfile1.read(1)
		c=dfile1.read(1)
		if nombre!=item:
			    dfile2.write(nombre+"\n")
		dfile2.close()
		dfile1.close()

	security.declarePublic("extraer2")
	def extraer2(self, contents, pos):
		#TODO Number 2
		i=0
		enters=0
		nombre=""
		while enters<pos+1:
			c=contents[i:i+1]
    		if c=="\n": 
    			enters=enters+1
	    	i=i+1
		c=contents[i:i+1]
		while c!="\n":
			nombre=nombre+c
			i=i+1
			c=contents[i:i+1]
		return nombre

	security.declarePublic("extraer")
	def extraer(self, contents, pos):
		#TODO Number 2
		i=0
		enters=0
		nombre=""
		while enters<pos+1:
			c=contents[i:i+1]
			if c=="\n": 
			    enters=enters+1
			    i=i+1
		c=contents[i:i+1]
		while c!="\n":
		    nombre=nombre+c
		    i=i+1
		    c=contents[i:i+1]
		return nombre
Globals.InitializeClass(FindAndManipulateLine)
