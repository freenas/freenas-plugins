import hashlib
import json
import os
import pwd
import urllib

from django.utils.translation import ugettext_lazy as _

from dojango import forms
from mediabrowserUI.freenas import models, utils


class MediaBrowserForm(forms.ModelForm):

    class Meta:
        model = models.MediaBrowser
        exclude = ('enable',)

    def __init__(self, *args, **kwargs):
        self.jail_path = kwargs.pop('jail_path')
        super(MediaBrowserForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        obj = super(MediaBrowserForm, self).save(*args, **kwargs)

        rcconf = os.path.join(utils.mediabrowser_etc_path, "rc.conf")
        with open(rcconf, "w") as f:
            if obj.enable:
                f.write('mediabrowser_enable="YES"\n')

        os.system(os.path.join(utils.mediabrowser_pbi_path, "tweak-rcconf"))
