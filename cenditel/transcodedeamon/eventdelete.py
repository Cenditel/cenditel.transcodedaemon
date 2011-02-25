#!/usr/bin/env python

#from cenditel.transcodedeamon.convert import ServiceList
from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo
from Acquisition import aq_parent

def type_custom_delete(object, evt):
    import pdb; pdb.set_trace()
    request = getattr(object, 'REQUEST', None)
    realDelete = False
    if request is None:
        realDelete = True
    else:
        info = ILinkIntegrityInfo(request) 
    if not info.integrityCheckingEnabled():
        realDelete = True 
    elif not info.getIntegrityBreaches():
        realDelete = True
    elif info.isConfirmedItem(object):
        realDelete = True
            
    if realDelete==True:
        pass
    if request.form.has_key('form.button.Cancel'):
            import pdb; pdb.set_trace()
            return request.RESPONSE.redirect('www.google.com') 
            """
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