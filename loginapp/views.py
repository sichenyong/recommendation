from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from loginapp.models import Sysusers
from recommendapp.utils import getPosition
# Create your views here.
def loginPage(request):
    return render(request,"loginapp/login.html")


@csrf_exempt
# 登录
# status: 0表示密码错误，1表示密码正确， 2表示用户不存在
def login(request):
    try:
        uname = request.POST.get('username')
        pword = request.POST.get('password')

        user = Sysusers.objects.get(account = uname)

        status = 0
        if pword == user.password:
            status = 1
            session_name = "user"
            request.session[session_name] = {"username":uname,"password":pword}
            request.session.set_expiry(0)
        
    except:
        status = 2
    data = {}
    data['status'] = status
    return JsonResponse({'data':data})

# 首页
def index(request):
    islogin = 0
    context = {}
    session = request.session.get("user","")
    if session is not "":
        user = Sysusers.objects.get(account = session["username"])
        islogin = 1
        context['user'] = user
    context['islogin'] = islogin

    return render(request,"index.html", context)

#加载注册页面
def reset(request):
    return render(request, "loginapp/register.html")

#注册
@csrf_exempt
def register(request):
    status = 0
    username = request.POST.get('username')
    password = request.POST.get('password')
    nickname = request.POST.get('nickname')
    age = request.POST.get('age')
    phone = request.POST.get('phone')
    #判断用户是否存在
    try:
        user = Sysusers.objects.get(account = username)
        status = 0
    except:
        ob = Sysusers()
        ob.account = username
        ob.password = password
        ob.nickname = nickname
        ob.age = age
        ob.phone = phone
        ob.save()
        status = 1

    context = {}
    context['status'] = status
    return JsonResponse({'data':context})

# 退出
def logout(request):
    #删除当前的会话数据
    request.session.flush()
    return redirect(reverse("index"))

def goProfile(request):
    userdata = request.session.get("user","")
    username = userdata["username"]
    user = Sysusers.objects.get(account = username)
    context = {}
    context['user'] = user
    return render(request,"user/userprofile.html",context)

@csrf_exempt
def update(request):
    uid = request.POST.get('user_id')
    uname = request.POST.get('username')
    pword = request.POST.get('password')
    nickname = request.POST.get('nickname')
    age = request.POST.get('age')
    gender = request.POST.get('sex')
    phone = request.POST.get('phone')
    email = request.POST.get('email')

    user = Sysusers.objects.get(user_id = uid)
    user.password = pword
    user.nickname = nickname
    user.age = age
    user.gender = gender
    user.phone = phone
    user.email = email
    user.save()
    return redirect(reverse("index"))