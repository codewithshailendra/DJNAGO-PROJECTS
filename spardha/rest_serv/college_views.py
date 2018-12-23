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
def CollegeView(request):
    if(request.method=='POST'):
        status = CheckRequiredFields(request, required_fields=['college_name'])
        if(status is not None):
            return status
        college = College.Create(name_field=request.POST['college_name'])
        if(college is None):
            return HttpResponse(json.dumps({"error":"true","detail":"college_exists"}), content_type="application/json")
        return HttpResponse(json.dumps({"error":"false","detail":"success","uid":college.CollegeID}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"error":"true","detail":"unsupported_request"}), content_type="application/json")
    return HttpResponse(json.dumps({"error":"true","detail":"bad_request"}), content_type="application/json")