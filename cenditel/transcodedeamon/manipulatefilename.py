####Este es un script de prueba para pasar la seguridad de Zope####
##bind context=context
# -*. coding ut8
#######################################
#python imports
import urlparse
import os
#######################################
#Zope imports
from AccessControl import ClassSecurityInfo, getSecurityManager
import Globals
from zope.interface import implements
from Acquisition import aq_inner
from zope.component import getMultiAdapter
#######################################
from cenditel.trancodedeamon import transcodedeamonMessageFactory as _


#Acquisition.interfaces.Interface


class ManipulateFileName:
    security = ClassSecurityInfo()

    """
    security.declarePublic("__init__")
    def __init__(self):
    	return
    """

    security.declarePublic('cmdpath')
    def cmdpath(self):
        """
        This method return the location of the file in execution
        """
        return os.system('pwd')

    security.declarePublic("TitleDeleteSpace")
    def TitleDeleteSpace(self, title):
	#antiguo dspace
	"""
        This method delete a firts space in the title of the content type
        """
        newtitle=""
        flag=1
	for x in title:
	    if x==" ":
        	if flag==0:
        	   newtitle=newtitle+x
        	   flag=1
            else:
               newtitle=newtitle+x
               flag=0
        if newtitle[len(newtitle)-1]==" ":
            newtitle=newtitle[:len(newtitle)-1]
        return newtitle


    security.declarePublic("DeleteSpaceinNameOfFolderFile")
    def DeleteSpaceinNameOfFolderFile(self,title):
        #Antiguo dfolder
        #this method return a new title replacing spaces ( ) for guions (-)
        #title=title.lower()
        newtitle=""
        for x in title:
            if x!=" ":
                newtitle=newtitle+x
            else:
                newtitle=newtitle+"-"
        return newtitle

    security.declarePublic("ReturnPathOfFile")
    def ReturnPathOfFile(self, url):
	"""
	This method find the folders in the hard drive using the urls from Plone
	"""
	count=0
	urlComponent = urlparse.urlparse(url)
	for part in urlComponent:
	    count = count + 1
	    if count == 3:
		FolderPath = part
	return FolderPath
    
    security.declarePublic("ReturnFileNameOfFileSaved")
    def ReturnFileNameOfFileSaved(self,STORAGE,path):
	#Antiguo dfilename
	#This method is for find in the fss.cfg and return the name of file saved        
	#title=self.DeleteSpaceinNameOfFolderFile(title);
	try:
	    file=open(STORAGE + path +'/fss.cfg','r');
	    cad=file.read();
	    return cad[19:len(cad)-2];
	except IOError:
	    ErrorDic={'ErrorMSG':_("Error open the configuration file" + STORAGE + path +/fss.cfg"), 'ErrorBol':True}
	    return  ErrorDic

    security.declarePublic('ReturnFileSizeOfFileInHardDrive')
    def ReturnFileSizeOfFileInHardDrive(self, variable): 
        #antiguo dfilesize
        """
        This method return the Size of the file in the Hard Drive
        """
        size=os.path.getsize(variable)
        if size<1024:
            return str("%3.0f"%(size))+"Bytes"
        else:
            if size<1048573:
                return str("%3.0f"%(size/1024))+"KBytes"
	    else:
		if size<1073741824:
		    return str("%3.0f"%(size/1048576))+"MBytes"
		else:
		    return str("%3.0f"%(size/1073741824))+"GBytes"
Globals.InitializeClass(ManipulateFileName)

if __name__=='__main__':
    print "manipulatefilename is loaded"