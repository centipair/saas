from django import forms
from django.conf import settings
from PIL import Image, ImageOps
import os
from core.utilities import unique_name


class ImageForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ImageForm, self).__init__(*args, **kwargs)

    def get_thumb_filename(self, filename):
        return settings.UPLOAD_PATH + "thumb_" + filename

    def format_image(self, filename, width, prefix):
        format_image_name = settings.UPLOAD_PATH + prefix + "_" + filename
        image = Image.open(settings.UPLOAD_PATH + filename)
        size = image.size
        prop = width / float(image.size[0])
        if int(prop * float(image.size[1])) > 600:
            prop = width / float(image.size[1])

        size = (int(prop * float(image.size[0])),
                int(prop * float(image.size[1])))
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(format_image_name, 'JPEG')
        return prefix + "_" + filename

    def crop_format_image(self, filename, width, height, prefix):
        format_image_name = settings.UPLOAD_PATH + prefix + "_" + filename
        image = Image.open(settings.UPLOAD_PATH + filename)
        THUMBNAIL_SIZE = (width, height)

        # Convert to RGB if necessary
        # Thanks to Limodou on DjangoSnippets.org
        # http://www.djangosnippets.org/snippets/20/
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        # scale and crop to thumbnail
        imagefit = ImageOps.fit(image, THUMBNAIL_SIZE, Image.ANTIALIAS)
        imagefit.save(format_image_name, 'JPEG')
        return prefix + "_" + filename

    def handle_uploaded_file(self, upload):
        upload_ext = os.path.splitext(upload.name)[1]
        generated_filename = unique_name(upload.name) + upload_ext
        upload_filename = settings.UPLOAD_PATH + generated_filename
        out = open(upload_filename, 'wb+')
        for chunk in upload.chunks():
            out.write(chunk)
        out.close()
        return generated_filename

    def delete_file(self, filename, prefixes):
        #try:
        if True:
            os.remove(settings.UPLOAD_PATH + filename)
            for prefix in prefixes:
                os.remove(settings.UPLOAD_PATH + prefix + "_" + filename)
        #except:
        #    pass
        return


class PageForm(forms.Form):
    site = forms
