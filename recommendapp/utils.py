#工具类
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
#聚类相关
from sklearn import preprocessing
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist  # 计算距离
import requests
import json
import time
# 聚类

#加载数据标准化工具
z_scaler = preprocessing.StandardScaler()

def get_lable(data, cluster_num) :
    #标准化
    data_z = z_scaler.fit_transform(data)
    data_z = pd.DataFrame(data_z)
    # 数据归一化
    minmax_scale = preprocessing.MinMaxScaler().fit(data_z)
    dataa = minmax_scale.transform(data_z)

    K = range(1, 11)

    meandistortions = []
    for k in K:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(dataa)
        meandistortions.append(
        sum(
            np.min(cdist(dataa, kmeans.cluster_centers_, 'euclidean'), axis=1)
        ) / dataa.shape[0]
    )
 
    """
    # 绘制碎石图
    plt.plot(K, meandistortions, 'bx--')
    plt.xlabel('k')
    plt.show()
    """
    
    k_means = KMeans(init='k-means++', n_clusters=cluster_num, max_iter=500)  # init='k-means++'表示用kmeans++的方法来选择初始质数 n_clusters=5表示数据聚为5类 max_iter=500表示最大的迭代次数是500(缺省300)
    k_means.fit(dataa)
    label = k_means.fit_predict(dataa)  # 聚类后的聚类标签放在label内
    return label

# 将label导出成列名为 column_name的数据表；然后将df与导出的数据表合并。最后按照lable排序
# 返回值 合并后且排好序的数据表
# 返回格式 数据表DataFrame
def dat_merge(df, label, column_name):
    dat_type = pd.DataFrame(label)  # 将模型结果导出为数据表
    dat_type.columns = [column_name]  # 设置列名
    dat = pd.merge(df, dat_type, left_index=True, right_index=True)  # 合并类别表和数据表
    pd.set_option('display.max_rows', None)
    return dat

#获取当前位置的经纬度以及城市名称
def getPosition():
    url = "http://httpbin.org/ip"  # 也可以直接在浏览器访问这个地址
    r = requests.get(url)  # 获取返回的值
    ip = json.loads(r.text)["origin"]  # 取其中某个字段的值

    url = f'http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query&lang=zh-CN'
    # 其中fields字段为定义接受返回参数，可不传；lang为设置语言，zh-CN为中文，可以传
    res = requests.get(url)		# 发送请求
    data = json.loads(res.text)
    print(data, end="\n")
    jsondata = [data["country"],data["lat"],data["lon"]]
    return jsondata

def getLatLon(address):
    url = 'https://restapi.amap.com/v3/geocode/geo' 
    params = {'key':'511fdc2aaee1c3937c5f6c84fced3b68',
              'address':address}
    res = requests.get(url,params)
    jd = json.loads(res.text)
    print(jd)
    location = jd['geocodes'][0]['location']
    ans = location.split(",")
    return ans

# 推荐
# 定义haversine公式向量化计算函数
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 地球半径，单位：千米
    # 将所有输入转换为数值类型
    lat1 = pd.to_numeric(lat1, errors='coerce')
    lon1 = pd.to_numeric(lon1, errors='coerce')
    lat2 = pd.to_numeric(lat2, errors='coerce')
    lon2 = pd.to_numeric(lon2, errors='coerce')
    # 将角度转换为弧度
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def TCM(processed_checkin_data, processed_venue_data, user_id, top_N, rating):
    target_rows = processed_checkin_data.loc[processed_checkin_data['user_id'] == user_id]
    # 获取当前位置的经纬度
    position = getPosition()
    latitude = position[1]
    longitude = position[2]
    #获取用户所属群组对组内访问过的地点的评分
    user_venue_category = processed_checkin_data[['user_id','venue_id','user_category']]
    merged_df = pd.merge(rating, user_venue_category, on=['user_id', 'venue_id'])
    filtered_df = merged_df[merged_df['user_category'] == target_rows['user_category'].values[0]]           
    # 计算群组内用户对每个地点的平均评分
    group_rating = filtered_df.groupby('venue_id')['rating'].mean().reset_index()
    #对评分取倒数，
    group_rating['rating'] = group_rating['rating'].rdiv(1)
    # 获取用户user_id属于某一类用户的概率 返回类型为series
    frequency = target_rows['user_category'].value_counts(normalize=True)
    # index是用户类别, value是user_id喜欢这类的概率
    # 构造最终结果
    result_list = []
    for index, value in frequency.iteritems():
        venue_ids = processed_checkin_data.loc[processed_checkin_data['user_category'] == index]['venue_id'].tolist()
        targetTopic_rows = processed_venue_data.loc[processed_venue_data['venue_id'].isin(venue_ids)]
        unique_topics = targetTopic_rows['topic'].drop_duplicates().tolist()
        #获取目标主题的所有地点，并计算距离
        for topic in unique_topics:
            #获取topic所对应的地点
            target_venues = processed_venue_data.loc[(processed_venue_data['topic'] == topic)]
            distances = haversine(latitude, longitude, target_venues['latitude'], target_venues['longitude'])
            #加权计算
            distances = distances / value
            res = pd.Series(distances.values, index=target_venues['venue_id'], name='cost')
            result_list.append(res)
    final_venues = pd.Series(pd.concat(result_list))
    final_venues_df = final_venues.reset_index().rename(columns={'index': 'venue_id', 0: 'cost'})
    # 将 final_venues_df 与 group_rating DataFrame 合并
    merged_df = final_venues_df.merge(group_rating, on='venue_id', how='left')
    merged_df['rating'].fillna(float('inf'), inplace=True)
    # 计算新的 cost 并存回 cost 列
    merged_df['cost'] = merged_df['cost'] * merged_df['rating']
    final_venues =  pd.Series(merged_df['cost'].values, index=merged_df['venue_id'])

    #从小到大排序
    sorted_final_venues = final_venues.sort_values(ascending=True)
    print("utils执行完毕")
    print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    return sorted_final_venues.head(top_N).index