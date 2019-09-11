"""Main product initializer
"""

######Atapi Import from archetypes
from Products.Archetypes import atapi
from Products.CMFCore import utils

######
# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.
from zope.i18nmessageid import MessageFactory
transcodedaemonMF = MessageFactory('cenditel.transcodedaemon')

#import config

#allow_module(convert)

# ModuleSecurityInfo('ftplib').declarePublic('FTP', 'all_errors',
#   'error_reply', 'error_temp', 'error_perm', 'error_proto')
# from ftplib import FTP
# allow_class(FTP)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
