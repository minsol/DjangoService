#!/usr/bin/env python
# coding=utf-8
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse


# 默认开启了csrf保护机制，本服务仅作自测使用，加上csrf_exempt去除掉csrf保护
@csrf_exempt
def sendRequest(request):
    print('get into get request')
    dct = {
            'GET': request.GET,
            'POST': request.POST,
            # 'Body': request.body,
            # 在Django的实现中，request.POST对象是用于存储包含表单数据的对象，而在request.body中则包含了content中的原始(raw)非表单数据
            }
    try:
        dct['json_parsed_body'] = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        print('json loads except:{}'.format(e))
    # return HttpResponse("Hello Django")
    return HttpResponse(HttpResponse(json.dumps(dct)), content_type='application/json')