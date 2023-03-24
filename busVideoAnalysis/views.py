# -*- coding:utf-8 -*-
"""
@Author:ddz
@Date:2023/3/24 13:51
@Project:views
"""
import logging

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
from .models import Image
# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
import os
from datetime import datetime
from .models import Image

from segmentBaseLpsnet import predict


def py2html(request):
    context = {"p2html": ["python 2 html", "python 2 js"]}
    return render(request, "index.html", context)


# 接收POST请求数据
def postexample(request):
    ctx ={}
    if request.POST:
        ctx['rlt'] = request.POST['q']
    return render(request, "postExample.html", ctx)


@csrf_exempt
def carclassify(request):
    img = list(Image.objects.all())[-1]
    path = predict.getMask(f".{img.img.url}")
    res = {"imgs": img, "label": path}

    return render(request, 'imgupload.html', res)


@csrf_exempt
def uploadImg(request):
    if request.method == 'POST':
        new_img = Image(
            img=request.FILES.get('img'),
            name=request.FILES.get('img').name,
            time=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        )
        new_img.save()
        return carclassify(request)
    return render(request, 'imgupload.html')