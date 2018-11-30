#!/usr/bin/env python
# coding=utf-8
from django.conf.urls import url
from . import views
 
 
urlpatterns = [
        url('', views.sendRequest),
    ]