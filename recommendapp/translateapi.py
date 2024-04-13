import hashlib
import time
import uuid

import requests

def youdaoTranslate(translate_text,flag=0):
    '''
    :param translate_text: 待翻译的句子
    :param flag: 1:原句子翻译成英文；0:原句子翻译成中文
    :return: 返回翻译结果
    '''
    youdao_url = 'https://openapi.youdao.com/api'  # 有道api地址

    # 翻译文本生成sign前进行的处理
    input_text = ""

    # 当文本长度小于等于20时，取文本
    if (len(translate_text) <= 20):
        input_text = translate_text

    # 当文本长度大于20时，进行特殊处理
    elif (len(translate_text) > 20):
        input_text = translate_text[:10] + str(len(translate_text)) + translate_text[-10:]

    time_curtime = int(time.time())  # 秒级时间戳获取
    app_id = "2bf6176da83f2277"  # 自己的应用id
    uu_id = uuid.uuid4()  # 随机生成的uuid数，为了每次都生成一个不重复的数。
    app_key = "YySsCLpYP5oflRQwgZJZ6PfD5tDBuJqR"  # 自己的应用密钥

    sign = hashlib.sha256(
        (app_id + input_text + str(uu_id) + str(time_curtime) + app_key).encode('utf-8')).hexdigest()  # sign生成

    data = {
        'q': translate_text,  # 翻译文本
        'appKey': app_id,  # 应用id
        'salt': uu_id,  # 随机生产的uuid码
        'sign': sign,  # 签名
        'signType': "v3",  # 签名类型，固定值
        'curtime': time_curtime,  # 秒级时间戳
    }
    if flag:
        data['from'] = "zh-CHS"  # 译文语种
        data['to'] = "en"  # 译文语种
    else:
        data['from'] = "en"  # 译文语种
        data['to'] = "zh-CHS"  # 译文语种

    r = requests.get(youdao_url, params=data).json()  # 获取返回的json()内容
    # print("翻译后的结果：" + r["translation"][0])  # 获取翻译内容
    return r["translation"][0]
