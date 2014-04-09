from django.utils.translation import ugettext as _
from django.http import HttpResponse
from centipair.core.template_processor import render_template


# Create your views here.

def page(request, url):
    return render_template(request, "index.html", base="base.html")
