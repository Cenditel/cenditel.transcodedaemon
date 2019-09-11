#!/usr/bin/env python

from os import path, listdir, remove
from zope.app.component.hooks import getSite
from iw.fss.config import ZCONFIG
from cenditel.transcodedaemon.convert import MTD

def ModifiedElement(object, evt):
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
    # import pdb; pdb.set_trace()
    file_object=object.getField(object.portal_type)
    name_original_file=file_object.getFilename(object)
    original_path=path.join(STORAGE,evt.object._getURL())
    # import pdb; pdb.set_trace()
    for file_name in listdir(original_path):
        # import pdb; pdb.set_trace()
        if (file_name == name_original_file) or (file_name =='fss.cfg') or (file_name == MTD.nginxpath(name_original_file)):
            pass
        else:
            remove(path.join(original_path,file_name ))
    return
