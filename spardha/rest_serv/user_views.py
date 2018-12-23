from django.shortcuts import render
from django.http import HttpResponse
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
def RegisterView(request):
    if(request.method=='POST'):
        status = CheckRequiredFields(request, required_fields=['email','password','name','college_name','mob_no'])
        if(status is not None):
            return status
        POST = request.POST
        player = Player.Register(email_field=POST['email'],password_field=POST['password'],name_field=POST['name'], 
                                mob_field=POST['mob_no'],college_name=POST['college_name'],image_field=None)
                                #TODO ADD IMAGE
        player.save()
        if(player is None):
            return HttpResponse(json.dumps({"error":"true","detail":"existing_user"}), content_type="application/json")
        return HttpResponse(json.dumps({"error":"false","detail":"successful","uid":repr(player.PlayerID)}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error":"true","detail":"unsupported_request"}), content_type="application/json")
    return HttpResponse(json.dumps({"error":"true","detail":"bad_request"}), content_type="application/json")

@csrf_exempt
def LoginView(request):
    if(request.method=='POST'):
        status = CheckRequiredFields(request, required_fields=['email','password'])
        if(status is not None):
            return status
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if(user is None):
            return HttpResponse(json.dumps({"error":"true","detail":"login_failed"}), content_type="application/json")
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
            token.save()
        return HttpResponse(json.dumps({"error":"false","detail":"login_success","token":token.key}), content_type="application/json")
    else:
        HttpResponse(json.dumps({"error":"true","detail":"unsupported_request"}), content_type="application/json")
    return HttpResponse(json.dumps({"error":"true","detail":"bad_request"}), content_type="application/json")
