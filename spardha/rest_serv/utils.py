import json
from django.http import HttpResponse

def CheckRequiredFields(request, required_fields):
    not_given = []
    for req in required_fields:
        if(req not in request.POST):
            not_given.append(req)
    if(len(not_given)!=0):
        return HttpResponse(json.dumps({"error":"true","detail":"incomplete_request","required":json.dumps(not_given)}), content_type="application/json")
    return None