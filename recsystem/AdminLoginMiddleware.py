from django.shortcuts import render,redirect
from django.http import HttpResponse
import re

from django.urls import reverse

class AdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        print(request.path)
        urllist = ['/admin/login','/admin/','/admin/dashboard']
        # 检测当前的请求是否已经登录,如果已经登录,.则放行,如果未登录,则跳转到登录页

        # 判断是否进入了后台,并且不是进入登录页面
        if re.match('/user/',request.path) and request.path not in urllist:

            # 检测session中是否存在 adminlogin的数据记录
            if request.session.get('user','') == '':
                # 如果在session没有记录,则证明没有登录,跳转到登录页面
                return HttpResponse('<script>alert("请先登录");window.location.href = "/loginpage";</script>')
        if re.match('/recommend/',request.path) and request.path not in urllist:
            # 检测session中是否存在 adminlogin的数据记录
            if request.session.get('user','') == '':
                # 如果在session没有记录,则证明没有登录,跳转到登录页面
                return HttpResponse('<script>alert("请先登录");window.location.href = "/loginpage";</script>')
        

        response = self.get_response(request)
        return response