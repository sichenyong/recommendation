from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from loginapp.models import Sysusers
from recommendapp.models import Venues,Venueflection
from django.core import serializers
from django.core.paginator import Paginator
import json
from recommendapp.utils import getLatLon
# Create your views here.

def loginPage(request):
    return render(request,"admin/login.html")

# status: 0 密码错误， 1表示登陆成功，2表示用户不存在，3表示没有权限！
@csrf_exempt
def login(request):
    try:
        uname = request.POST.get('username')
        pword = request.POST.get('password')
        user = Sysusers.objects.get(account = uname)
        user = Sysusers.objects.get(account = uname)
        status = 0

        if user.type == 1 and pword == user.password:
            status = 1
            session_name = "admin"
            request.session[session_name] = {"username":uname,"password":pword}
            request.session.set_expiry(0)
        
        if user.type == 0:
            status = 3
    except:
        status = 2
    data = {}
    data['status'] = status
    return JsonResponse({'data':data})

# 控制中心
def dashboard(request):
    context = {}
    context["status"] = 0

    return render(request,"admin/dashboard.html",context)

@csrf_exempt
def getSysUser0(request):
    page = int(request.GET.get("page"))
    limit = int(request.GET.get("limit"))
    print("page = " + str(page))
    print("limit = " + str(limit))
    # 获取普通用户
    users = Sysusers.objects.filter(type__exact = 0)
    count = len(users)
    p = Paginator(users,limit)
    if page < 1:
        page = 1
    if page > p.num_pages:
        page = p.num_pages

    users = p.page(page)
    
    sysusers = serializers.serialize("json",users,ensure_ascii=False)
    sysusers = json.loads(sysusers)
    dlist = []
    for user in sysusers:
        tmp = user["fields"]
        tmp['user_id'] = user["pk"]
        dlist.append(tmp)

    data = {
        "users":dlist,
        "count":count
    }
    return JsonResponse(data,safe=False,json_dumps_params={'ensure_ascii': False})

def sys1user(request):
    context = {}
    context["status"] = 0

    return render(request,"admin/sysdashboard.html",context)

@csrf_exempt
def getSysUser1(request):
    page = int(request.GET.get("page"))
    limit = int(request.GET.get("limit"))

    # 获取系统用户
    users = Sysusers.objects.filter(type__exact = 1)
    count = len(users)
    p = Paginator(users,limit)
    if page < 1:
        page = 1
    if page > p.num_pages:
        page = p.num_pages

    users = p.page(page)
    
    sysusers = serializers.serialize("json",users,ensure_ascii=False)
    sysusers = json.loads(sysusers)
    dlist = []
    for user in sysusers:
        tmp = user["fields"]
        tmp['user_id'] = user["pk"]
        dlist.append(tmp)

    data = {
        "users":dlist,
        "count":count
    }
    return JsonResponse(data,safe=False,json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def usereditPage(request,user_id):
    user = Sysusers.objects.get(user_id = user_id)
    context = {
        'status':0,
        'user':user
    }
    return render(request,"admin/usereditPage.html",context)
@csrf_exempt
def doeditUser(request):
    uid = request.POST.get('userid')
    pwd = request.POST.get('password')
    nickname = request.POST.get('nickname')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    phone = request.POST.get('tel')
    email = request.POST.get('email')
    type = request.POST.get('type')

    user = Sysusers.objects.get(user_id = uid)
    if user.type == 0:
        href = "dashboard"
    else:
        href = "sysdashboard"
    user.password = pwd
    user.nickname = nickname
    user.age = age
    user.gender = gender
    user.phone = phone
    user.email = email
    user.type = type
    user.save()
    url = '<script>alert("修改成功");window.location.href = "' + href + '";</script>'
    return  HttpResponse(url)

#删除用户
def userdel(request,user_id):
    user = Sysusers.objects.get(user_id = user_id)
    user.delete()
    type = user.type
    if type == 0:
        context = {}
        context["status"] = 0
        return render(request,"admin/dashboard.html",context)
    else:
        context = {}
        context["status"] = 1
        return render(request,"admin/sysdashboard.html",context)
    
# 用户搜索
@csrf_exempt
def usersearch(request):
    page = int(request.GET.get("page"))
    limit = int(request.GET.get("limit"))
    type = request.GET.get('type')
    kw = request.GET.get('key')
    kw2 = request.GET.get('key2')
    user_queryset = Sysusers.objects.filter(account__contains = kw).filter(nickname__contains = kw2).filter(type__exact = type)
    count = len(user_queryset)
    p = Paginator(user_queryset,limit)
    if page < 1:
        page = 1
    if page > p.num_pages:
        page = p.num_pages

    #获取当前页面的用户
    users = p.page(page)
    
    users = serializers.serialize("json",users,ensure_ascii=False)
    users = json.loads(users)
    dlist = []
    for user in users:
        tmp = user["fields"]
        tmp['user_id'] = user["pk"]
        dlist.append(tmp)

    data = {
        "users":dlist,
        "count":count
    }
    return JsonResponse(data,safe=False,json_dumps_params={'ensure_ascii': False})

# 添加用户
def adduserPage(request):
    context = {}
    context["status"] = 0
    return render(request,"admin/adduserPage.html",context)
@csrf_exempt
def doadduser(request):
    account = request.POST.get('account')
    pwd = request.POST.get('password')
    nickname = request.POST.get('nickname')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    phone = request.POST.get('tel')
    email = request.POST.get('email')
    type = request.POST.get('type')
    

    ob = Sysusers()
    ob.account = account
    ob.password = pwd
    ob.nickname = nickname
    ob.age = age
    ob.gender = gender
    ob.phone = phone
    ob.email = email
    ob.type = type
    ob.save()
    context = {
        'status':0
    }
    return  render(request,"admin/dashboard.html",context)

@csrf_exempt
# 返回1表示用户已经存在
def userisexist(request):
    account = request.POST.get("account","")
    context = {
        'status':0
    }
    try:
        Sysusers.objects.get(account = account)
        context['status'] = 1
    except:
        pass
    return JsonResponse({'data':context})
    


# --------------------------------------------------------------景点操作---------------------------------
# 地点控制中心
def venueDashboard(request,pIndex=1):
    context = {}
    context["status"] = 1

    list = Venues.objects.filter()

    p = Paginator(list,20)
    #判断页码值是否有效(防止越界)
    if pIndex<1:
        pIndex = 1
    if pIndex > p.num_pages:
        pIndex = p.num_pages
    
    vlist = p.page(pIndex)
    context["venuelist"] = vlist
    context["pIndex"] = pIndex
    context["pageNum"] = p.num_pages
    return render(request,"admin/venuedashboard.html",context)

# 修改地点
def editvenue(request,venue_id):
    venue = Venues.objects.get(venue_id = venue_id)
    context = {}
    context["status"] = 1
    context["venue"] = venue

    return render(request,"admin/venueedit.html",context)

@csrf_exempt
def doeditvenue(request):

    venue_id = request.POST.get('vid')
    venue_name = request.POST.get('vname')
    latitude = request.POST.get('lat')
    longitude = request.POST.get('lon')
    introducoty = request.POST.get('inc')

    ob = Venues.objects.get(venue_id = venue_id)
    ob.venue_name = str(venue_name)
    ob.latitude = float(latitude)
    ob.longitude = float(longitude)
    ob.introducoty = str(introducoty)
    ob.save()

    return HttpResponse('<script>alert("修改成功");window.location.href = "venuedashboard/1";</script>')

# 删除
def delvenue(request, venue_id):
    ob = Venues.objects.get(venue_id = venue_id)
    ob.delete()
    return HttpResponse("<h1>删除成功！</h1>")

@csrf_exempt
def venuesearch(request):
    vid = request.POST.get('vid')
    vname = request.POST.get('vname')
    context = {}
    context["status"] = 1
    venue_list = []
    if vid != "":
        try:
            venue = Venues.objects.get(venue_id = vid)
            venue.venue_id = int(venue.venue_id)
            venue_list.append(venue)
        except:
            pass
    if vname != "":
        try:
            venue = Venues.objects.get(venue_name = vname)
            venue.venue_id = int(venue.venue_id)
            venue_list.append(venue)
        except:
            pass

    if len(venue_list) == 0:
        return HttpResponse("查找不存在!")
    context["venuelist"] = venue_list
    context["pIndex"] = 1
    context["pageNum"] = 1

    return render(request,"admin/venuedashboard.html",context)

def addvenue(request):
    context = {}
    context["status"] = 1
    return render(request,"admin/addvenue.html",context)

@csrf_exempt
def doaddvenue(request):
    venue_name = request.POST.get('vname')
    inc = request.POST.get('inc')
    lists = getLatLon(venue_name)
    ob = Venues()
    ob.venue_name = venue_name
    ob.latitude = float(lists[0])
    ob.longitude = float(lists[1])
    ob.introducoty = str(inc)
    print(venue_name)
    print(inc)
    ob.save()

    return HttpResponse('<script>alert("添加成功");window.location.href = "1";</script>')

# 退出
def logout(request):
    request.session.flush()
    return redirect(reverse("index"))

# 管理员个人界面
def adminPage(request):
    session_data = request.session.get("admin","")
    username = session_data["username"]
    user = Sysusers.objects.get(account = username)
    context = {
        'status':0,
        'user':user
    }
    return render(request,"admin/usereditPage.html",context)

