import re

from z3c.form import interfaces

from zope import schema
from zope.interface import Interface

from plone.theme.interfaces import IDefaultPloneLayer

try:
    from cenditel.video.config import CONTROL as video
except ImportError:
    video=0

try:
    from cenditel.audio.config import CONTROL as audio
except ImportError:
    audio=0

from cenditel.transcodedeamon import transcodedeamonMF as _

    
class IThemeSpecific(IDefaultPloneLayer):
        """Marker interface that defines a Zope 3 browser layer."""


class ITranscodeSetings(Interface):
    """This discribed the configuration of transcode deamon. You can start or shutdown the configuration of transcode, change the parametres of work the dependecie ffmpeg
    """
   
    transcode_switch = schema.Bool(
        title=_(u"Transcode Switch"),
        description=_(u"Specifies if the transcode is ON or OFF, default is ON"),
        default=True,
    )

    adress_of_streaming_server = schema.Text(
        title=_(u"The adress of the streaming server, must be a Web server to publish the multimedia contents"),
        description=_(u"Enter the URL to the streaming server"),
        default=u'http://localhost:80',
        required=True,
    )
    
    mount_point_fss = schema.Text(
        title=_(u"The mount point of File System Storage"),
        description=_(u"Enter the path of the mount point"),
        default=u'/home/Plone',
        required=True,
    )
    
    max_file_size = schema.Int(
        title=_(u"The max file size that can be uploaded"),
        description=_(u"Enter the max file size, in MB (like 30)"),
        required=True,
        default = 30,
        min = 5,
        max = 1024
    )

    if audio==1:
        ffmpeg_parameters_video_line = schema.Text(
            title=_(u"Parameters of FFMPEG to use in video transcode"),
            description=_(u"This line has all the parameters to use in FFMPEG to convert files between formats, by default, this services have been preconfigured with following parameters ' -b 926k -aspect 16:9 -vframes 25000 -vcodec libtheora -acodec libvorbis -ab 128k -ac 2 -ar 48000'. Optionally are others recommended FFMPEG parameters useful like ' -b 200k -aspect 16:9 -vframes 25000 -vcodec libtheora -acodec libvorbis -ab 100k -ac 2 -ar 48000' and ' -aspect 16:9 -sameq -vcodec libtheora -acodec libvorbis -ab 100k+'."),
            default=u'-b 926k -aspect 16:9 -vframes 25000 -vcodec libtheora -acodec libvorbis -ab 128k -ac 2 -ar 48000',
            required=True,
        )

        video_valid_content_types = schema.Text(
            title=_(u"Video Valid Content Types to be uploaded"),
            description=_(u"Those are the valid content types that can be uploaded to the server using Cenditel multimedia products, to load a new content type the mimetype must have a space after him"),
            default=u'video/3gpp video/mpeg video/quicktime video/x-flv video/x-mng video/x-ms-wmv video/x-msvideo video/ogg video/mp4 video/x-ms-wmv ',
            required=True,
        )
    else:
        pass
    if video==1:
        ffmpeg_parameters_audio_line = schema.Text(
            title=_(u"Parameters of FFMPEG to use in audio transcode"),
            description=_(u"This line has all the parameters to use in FFMPEG to convert files between formats, by default, this services have been preconfigured with following parameters ' -b 926k -aspect 16:9 -vframes 25000 -vcodec libtheora -acodec libvorbis -ab 128k -ac 2 -ar 48000'. Optionally are others recommended FFMPEG parameters useful like ' -b 200k -aspect 16:9 -vframes 25000 -vcodec libtheora -acodec libvorbis -ab 100k -ac 2 -ar 48000' and ' -aspect 16:9 -sameq -vcodec libtheora -acodec libvorbis -ab 100k+'."),
            default=u'-acodec libvorbis -ab 128k -ac 2 -ar 48000',
            required=True,
        )

        audio_valid_content_types = schema.Text(
            title=_(u"Video Valid Content Types to be uploaded"),
            description=_(u"Those are the valid content types that can be uploaded to the server using Cenditel multimedia products, to load a new content type the mimetype must have a space after him"),
            default=u'audio/midi audio/mpeg audio/x-realaudio ',
            required=True,
        )
    else:
        pass
        
