from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.views.generic import CreateView

from django.contrib.messages.views import SuccessMessageMixin

from MajorApp.models import UrlModel, Result
from MajorApp.forms import UrlForm

import shutil
from screenshotone import Client, TakeOptions

import json
import requests
import urllib



# Create your views here.
def index(request):
    return render(request, 'index.html')

class UrlCreate(SuccessMessageMixin, CreateView):
    model = UrlModel
    form_class = UrlForm
    template_name = 'url.html'
    success_url = reverse_lazy('result')
    success_message = "Url added successfully"


def scanUrl(request):
    r = Result()
    url = UrlModel.objects.last()
    strictness = 0
    additional_params = {
        'strictness': strictness
    }
    ipqs = IPQS()
    result = ipqs.malicious_url_scanner_api(url.url, additional_params)
    client = Client('SAloNjtB-K5eNA', 'pk8eGYQvTHgTUw')

    # set up options
    options = (TakeOptions.url(str(url.url))
        .format("png")
        .viewport_width(1024)
        .viewport_height(768)
        .block_cookie_banners(True)
        .block_chats(True))

    # or render a screenshot and download the image as stream
    image = client.generate_take_url(options)
    r.phishing = result['phishing']
    r.success = result['success']
    r.domain = result['domain']
    r.risk_score = result['risk_score']
    r.category = result['category']
    r.malware = result['malware']
    r.screenshot = image
    r.save()
    context = {
        'results': Result.objects.all(),
    }
    return render(request, 'result.html', context=context)

class IPQS():
    key = 'YhCEJ9WiyT8PjWDWGynbZ8LphEG1U9eJ'

    def malicious_url_scanner_api(self, url: str, vars: dict = {}) -> dict:
        url = 'https://www.ipqualityscore.com/api/json/url/%s/%s' % (self.key, urllib.parse.quote_plus(url))
        x = requests.get(url, params=vars)
        return (json.loads(x.text))


