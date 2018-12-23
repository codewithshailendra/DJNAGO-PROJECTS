from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
#from .serializers import *
import json
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from .utils import *

@csrf_exempt
@api_view(['GET'])
def EventView(request):
    if(request.method=='GET'):
        if('id' in request.GET):
            try:
                event = Event.get(request.GET['id'])
            except:
                return HttpResponse(json.dumps({'detail':'no_such_event'}), status=404)
            return JsonResponse(Event)
        elif('date' in request.GET):
            
        else:
            return HttpResponse(json.dumps({'detail':'unsupported_request_parameter'}), status=400)
    else:
        return HttpResponse(json.dumps({'detail':'unsupported_request'}), status=400)
    return HttpResponse(json.dumps({'detail':'bad_request'}), status=400)