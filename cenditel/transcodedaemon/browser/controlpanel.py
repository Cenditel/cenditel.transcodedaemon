# python import
import os
import urlparse

# zope import
from Products.Five.browser import BrowserView
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from plone.app.registry.browser import controlpanel

# product import
from cenditel.transcodedaemon.interfaces import ITranscodeSetings, _


class MultimediaPanelSettingsEditForm(controlpanel.RegistryEditForm):

    schema = ITranscodeSetings
    label = _(u"Cenditel Transcode Daemon Settings")
    description = _(u"This panel permits config some options of cenditel.transcodedaemon")

    def updateFields(self):
        super(MultimediaPanelSettingsEditForm, self).updateFields()
        

    def updateWidgets(self):
        super(MultimediaPanelSettingsEditForm, self).updateWidgets()


class CenditelMultimediaSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = MultimediaPanelSettingsEditForm
