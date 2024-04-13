import datetime
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from recommendapp.models import Checkins,Users,Venues,Venuetopic,Ratings
from loginapp.models import Sysusers
from recommendapp.utils import get_lable,dat_merge,TCM,getPosition
from django.views.decorators.csrf import csrf_exempt
# 地址转换
from recommendapp.translateapi import youdaoTranslate
from opencage.geocoder import OpenCageGeocode
import pandas as pd
import time
# Create your views here.
def recommend(request):
    #定义所需要的前缀
    prefix = ["star","pic","ratval","venue"]

    userdata = request.session.get("user","")
    username = userdata["username"]
    targetuser = Sysusers.objects.get(account__exact = username).user_id
    # 读取用户签到数据
    checkins = Checkins.objects.all().values_list("user_id","venue_id","latitude","longitude")
    checkin_data = pd.DataFrame(list(checkins),columns=["user_id","venue_id","latitude","longitude"])
    # 数据清洗
    checkin_data.dropna(axis=0, how="any", inplace= True)
    smaller_checkin_data = checkin_data.drop(axis=1, columns='venue_id', inplace=False)
    #群组划分
    user_label = get_lable(smaller_checkin_data,5)
    processed_checkin_data = dat_merge(checkin_data,user_label,'user_category')

    #获取处理好的地点主题信息
    venue_topic_queryset = Venuetopic.objects.all().values_list("venue_id","latitude","longitude","venue_category","topic")
    venue_topic = pd.DataFrame(list(venue_topic_queryset),columns=["venue_id","latitude","longitude","venue_category","topic"])
    topN = 10
    # 获取评分信息
    ratings_data_queryset = Ratings.objects.all().values_list("user_id","venue_id","rating")
    ratings_data = pd.DataFrame(list(ratings_data_queryset),columns=["user_id","venue_id","rating"])

    topN_venues = TCM(processed_checkin_data, venue_topic,targetuser,topN, ratings_data)
 
    context = {}
    # 地理处理工具
    key = "e3ba590c483f44dbbb94d230d0de7c8d"
    geocoder = OpenCageGeocode(key)
    # 存放位置名称
    loactions = []
    # 存放评分id
    stars = []
    # 存放图片轮播id
    ids = []
    # 存放评分值对应的id，在js中取值
    ratval = []
    # 存放地点id
    venueids = []
    # 存放地点介绍
    introductories = []
    for venue_id in topN_venues:
        venue = Venues.objects.get(venue_id__exact = venue_id)
        introductories.append(venue.introducoty)
        location = geocoder.reverse_geocode(venue.latitude,venue.longitude)
        loactions.append(youdaoTranslate(location[0]['formatted']))
    
    for i in range(1,topN + 1):
        stars.append(prefix[0] + str(i))
        ids.append(prefix[1] + str(i))
        ratval.append(prefix[2] + str(i))
        venueids.append(prefix[3] + str(i))

    #存放topn个地点的平均评分
    ratings = []
    for venue_id in topN_venues:
        target_rows = ratings_data.loc[ratings_data['venue_id'] == venue_id]
        ratings.append(target_rows['rating'].mean())
    
    ratings = [float('{:.1f}'.format(i)) for i in ratings]
    data = zip(topN_venues,stars,ratings,loactions,introductories,ids,ratval,venueids)

    context['title'] = "专属推荐"
    context['data'] = data
    context['islogin'] = 1
    context['user'] = Sysusers.objects.get(account__exact = username)
    print("即将渲染视图")
    print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    return render(request, "recommend/index.html", context)

# 推荐热门地点
def getHotVenues(request):
    prefix = ["star","pic","ratval","venue"]
    context = {}
    userdata = request.session.get("user","")
    username = userdata["username"]
    topN = 10

    # 获取评分信息
    ratings_data_queryset = Ratings.objects.all().values_list("user_id","venue_id","rating")
    ratings_data = pd.DataFrame(list(ratings_data_queryset),columns=["user_id","venue_id","rating"])
    ratings_data.drop(columns="user_id",inplace=True)
    ratings_data = ratings_data.groupby(by='venue_id').mean()
    df = ratings_data.sort_values(by='rating',ascending=False)
    hotvenues = list(df.head(topN).index)
    
    ratings = [float('{:.1f}'.format(value)) for value in list(df.head(topN)["rating"])]
    # 地理处理工具
    key = "e3ba590c483f44dbbb94d230d0de7c8d"
    geocoder = OpenCageGeocode(key)
    # 存放位置名称
    loactions = []
    # 存放评分id
    stars = []
    # 存放图片轮播id
    ids = []
    # 存放评分值对应的id，在js中取值
    ratval = []
    # 存放地点id
    venueids = []
    # 存放地点介绍
    introductories = []
    for venue_id in hotvenues:
        venue = Venues.objects.get(venue_id__exact = venue_id)
        introductories.append(venue.introducoty)
        location = geocoder.reverse_geocode(venue.latitude,venue.longitude)
        loactions.append(youdaoTranslate(location[0]['formatted']))

    for i in range(1,topN + 1):
        stars.append(prefix[0] + str(i))
        ids.append(prefix[1] + str(i))
        ratval.append(prefix[2] + str(i))
        venueids.append(prefix[3] + str(i))


    
    data = zip(hotvenues,stars,ratings,loactions,introductories,ids,ratval,venueids)
    context['data'] = data
    context['islogin'] = 1
    context['title'] = "热门地点"
    context['user'] = Sysusers.objects.get(account__exact = username)
    return render(request, "recommend/index.html", context)

@csrf_exempt
def doRating(request):
    rating = request.POST.get("rating")
    venue_id = request.POST.get("venue_id")

    ob = Ratings()
    ob.venue_id = int(venue_id)
    ob.rating = rating
    ob.user_id = int(Sysusers.objects.get(account__exact = request.session.get("user","")["username"]).user_id)
    ob.save()

    checkin = Checkins()
    checkin.venue_id = venue_id
    checkin.user_id = Sysusers.objects.get(account__exact = request.session.get("user","")["username"]).user_id
    checkin.create_at = datetime.datetime.now()
    position = getPosition()
    checkin.latitude = position[1]
    checkin.longitude = position[2]
    print(checkin)
    checkin.save()

    context = {}
    context['status'] = 1
    return JsonResponse({'data':context})

@csrf_exempt
def search_venue(request):
    venue_name = request.POST.get("venue_name")
    try:
        venue = Venues.objects.get(venue_name = venue_name)
    except:
        return HttpResponse('<h1>搜索的地址不存在')
    context = {}
    context['status'] = 1
    context['venue'] = venue
    context['url'] = "/static/images/" + str(venue.venue_id)
    print(context['url'])
    return render(request,'recommend/venue.html',context)