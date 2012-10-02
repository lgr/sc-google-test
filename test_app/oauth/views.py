# encoding:utf-8

import os
import httplib2

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from apiclient.discovery import build
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

from test_app import settings
from models import *


CLIENT_SECRETS = os.path.join(os.path.dirname(__file__),
                              '..', 'client_secrets.json')
FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
#    scope='https://www.googleapis.com/auth/plus.me',
    scope='https://www.googleapis.com/auth/analytics.readonly',
    redirect_uri='http://localhost:8000/oauth2callback')


def get_credential(user):
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    return storage.get()


@login_required
def home(request):
    # store and retrieve Credentials objects using a model 
    # defined with a CredentialsField object
    credential = get_credential(request.user)
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        print "NEW CREDENTIAL REQUESTED", FLOW.params['state']
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("analytics", "v3", http=http)
        # Get a list of all Google Analytics accounts for this user
        accounts = service.management().accounts().list().execute()
        """
        activities = service.activities()
        activitylist = activities.list(collection='public',
                                       userId='me').execute()
        print activitylist
        """
        context = { 'items': accounts['items'], }
        print context
        return render_to_response('oauth/index.html', context,
                   context_instance=RequestContext(request))


def widget_process(request):
    # Assumption: this function is called only when the user 
    # is already authenticated and successfully acomplished the acquisition
    # of the token
    permitted_calls = ['/management/accounts/list', ]
    if request.user.is_authenticated():
        try:
            api_call = request.GET['call']
            credential = get_credential(request.user)
            if api_call not in permitted_calls or credential is None:
                raise Exception()
            else:
                http = httplib2.Http()
                http = credential.authorize(http)
                service = build("analytics", "v3", http=http)
                real_call = '.'.join([elem + '()'
                                      for elem in api_call.split('/') if elem])
                result = eval('service.' + real_call + '.execute()')
                print result
                return HttpResponse(result, content_type='application/json')
        except:
            pass
    return HttpResponseForbidden()



@login_required
def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY,
                                   request.REQUEST['state'],
                                   request.user):
        return  HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/")
