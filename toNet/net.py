import datetime, hashlib, hmac
import requests  # Command to install: `pip install request`
import json
from requests_toolbelt import MultipartEncoder

AppKey = '3a5fd86050b311eb824a27307f107a44'


def r2t(filepath, ext):
    print("--------------------------------r2t-------------------------------------")
    # filepath = "/home/yxl/文档/比赛/xwq/人机对话/item99/第四单元任务实施1测试音频.wav"
    print("测试文件绝对路径：" + filepath)
    url = 'https://gwgray.tvs.qq.com/ai/asr'

    headers = {
        'Appkey': AppKey,
        'Content-Type': 'multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
    }
    payload = json.dumps({  # json.dumps() 是把python对象转换成json对象的一个过程，生成的是字符串
        "payload": {
            "audioMeta": {
                "format": ext,  # 音频格式: pcm/wav/amr/opus/mp3
                "sampleRate": "16K",  # 采样率: 8K/16K
                "channel": 1,  # 音频通道数: 1/2
                "lang": "zh-CN"  # 语言类型, 中文: zh-CN, 英文: en-US
            },
            "offset": 0,  # 语音片在语音流中的偏移
            "needPunc": True,  # 是否加标点
            "transNum": True,  # 是否开启文字转数字, 如一二三 to 123
            "useCloudVad": True,  # 是否使用云端vad, 由云端来停止语音，调用方不用发送 'finished'
            "vadThreshold": 111150,  # 云端vad静音阈值, 建议设置500, 单位ms
            "finished": True  # 语音是否结束
        }
    })
    data = MultipartEncoder(  # 封装的请求数据
        fields={
            "audio": (None, open(filepath, 'rb'), 'audio/' + ext),
            # form-data; name="audio"; filename="/D:/123/voiceprint.3.wav" 字段为audio,文件名的key是filename,类型是audio/mp3
            "metadata": (None, payload, "application/json; charset=utf8"),  # form-data; name="metadata"
        }, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW"
    )
    r = requests.post(url, data=data, headers=headers)
    print(r.text)
    if not json.loads(r.text)["header"]["code"] == 200:
        return json.loads(r.text)["header"]["message"]
    print("识别到的文字：" + json.loads(r.text)["payload"]["text"])  # 是将字符串传化为字典
    return json.loads(r.text)["payload"]["text"]


def p2t(filepath):
    print("--------------------------------p2t-------------------------------------")
    # filepath = "/home/yxl/文档/比赛/xwq/人机对话/item99/第四单元任务实施1测试音频.wav"
    print("测试文件绝对路径：" + filepath)
    url = 'https://gwgray.tvs.qq.com/ai/ocr/recognize'

    headers = {
        'Appkey': AppKey,
        'Content-Type': 'multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
    }
    payload = json.dumps({  # json.dumps() 是把python对象转换成json对象的一个过程，生成的是字符串
        "payload": {
            "imageUrl": "",  # 图片URL metadata中json字段"payload.imageUrl"不用填
            "type": 3,  # 识别类型  3快速识别
        }
    })
    data = MultipartEncoder(  # 封装的请求数据
        fields={
            "image": (None, open(filepath, 'rb'), 'image'),
            # form-data; name="audio"; filename="/D:/123/voiceprint.3.wav" 字段为audio,文件名的key是filename,类型是audio/mp3
            "metadata": (None, payload, "application/json; charset=utf8"),  # form-data; name="metadata"
        }, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW"
    )
    r = requests.post(url, data=data, headers=headers)
    if not json.loads(r.text)["header"]["code"] == 200:
        return json.loads(r.text)["header"]["message"]
    # print(r.text)
    return json.loads(r.text)["payload"]["ocrItems"][0]["text"]


def ok_text(text):
    print("--------------------------------ok_text--------------------------------------")
    # filepath = "/home/yxl/文档/比赛/xwq/人机对话/item99/第四单元任务实施1测试音频.wav"
    print("测试文本：" + text)
    url = 'https://gwgray.tvs.qq.com/ai/sensitive-detect'

    headers = {
        'Appkey': AppKey,
        'Content-Type': 'application/json'
    }
    payload = json.dumps({  # json.dumps() 是把python对象转换成json对象的一个过程，生成的是字符串
        "payload": {
            "content": text,  # 要检测的文本, 请使用 UTF-8 字符集
            "type": 0,  # 测什么类型
        }
    })
    r = requests.post(url, data=payload, headers=headers)
    print(r.text)
    return json.loads(r.text)["payload"]["status"]


def your(filepath, text, ext):
    print("-------------------------------your-------------------------------------")
    print("测试文件绝对路径：" + filepath)
    url = 'https://gwgray.tvs.qq.com/ai/evaluate/speech/sentence-once'
    accessToken = b'3a7c1bb9276b415d8c1d4524db29107c'
    appkey = '2df557605dc411ed87adc50dabda4409'
    payload = json.dumps({  # json.dumps() 是把python对象转换成json对象的一个过程，生成的是字符串
        "payload": {
            "audioMeta": {
                "format": ext,  # 音频格式: pcm/mp3
            },
            "text": text,
            "sEngine": "",
            "tightness": 0,
            "questionId": "book1-exam2-quest3",
        }
    })
    data = MultipartEncoder(  # 封装的请求数据
        fields={
            "audio": (None, open(filepath, 'rb'), 'audio/' + ext),
            # form-data; name="audio"; filename="/D:/123/voiceprint.3.wav" 字段为audio,文件名的key是filename,类型是audio/mp3
            "metadata": (None, payload, "application/json; charset=utf8"),  # form-data; name="metadata"
        }, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW"
    )
    credentialDate = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')  # 获得当前时间戳，样例格式为2021 04 09 T 02 45 11 Z
    signingContent = data.encoding + credentialDate  # 为签名原始数据,由   请求数据Json字符串   +    时间戳构成

    # 把"签名原始数据"signingContent用accessToken进行加密，加密方式为sha256，等于是创建了特定格式的鉴权信息
    signature = hmac.new(accessToken, signingContent.encode('utf8'), hashlib.sha256).hexdigest()  # 作为十六进制数据字符串值 加密

    # 计算得到签名之后，需要在请求头中带上签名信息，结构：加密方式+appkey+当前时间戳+签名信息组成鉴权信息
    authorizationHeader = 'TVS-HMAC-SHA256-BASIC' + ' ' + 'CredentialKey=' + appkey + ', ' + 'Datetime=' + credentialDate + ', ' + 'Signature=' + signature

    # 封装请求头：数据请求格式+鉴权信息
    headers = {'Content-Type': 'multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
               'DSN': '28:37:13:05:4A:4C',
               'appkey': appkey,
               'Authorization': authorizationHeader}

    r = requests.post(url, data=data, headers=headers)
    print(r.text)
    if not json.loads(r.text)["header"]["code"] == 200:
        result = {"status": True, "msg": json.loads(r.text)["header"]["message"]}
        return json.dumps(result, ensure_ascii=False)
    print("识别到的文字：" + json.loads(r.text)["payload"]["score"])  # 是将字符串传化为字典

    result = {"status": True,
              "score": json.loads(r.text)["payload"]["score"],
              "fluency": json.loads(r.text)["payload"]["fluency"],
              "integrity": json.loads(r.text)["payload"]["integrity"],
              "pronunciation": json.loads(r.text)["payload"]["pronunciation"],
              "rhythm": json.loads(r.text)["payload"]["rhythm"]}
    return json.dumps(result, ensure_ascii=False)


def flower(filepath, ext):
    print("-------------------------------flower------------------------------------")
    print("测试文件绝对路径：" + filepath)
    url = 'https://gwgray.tvs.qq.com/ai/image/flower'
    # 封装请求头：数据请求格式+鉴权信息
    headers = {'Content-Type': 'Content-Type: image/jpeg',
               'Appkey': AppKey}

    data = open(filepath, 'rb')
    print(type(data))
    r = requests.post(url, data=data, headers=headers)

    if not json.loads(r.text)["header"]["code"] == 200:
        result = {"status": False, "msg": json.loads(r.text)["header"]["message"]}
        return json.dumps(result, ensure_ascii=False)
    print("识别到的文字：" + json.loads(r.text)["payload"]["items"][0]["id"])  # 是将字符串传化为字典

    if json.loads(r.text)["payload"]["items"][0]["id"] == "":
        result = {"status": False,
                  "msg": "未识别到"}
        return json.dumps(result, ensure_ascii=False)
    result = {"status": True,
              "id": json.loads(r.text)["payload"]["items"][0]["id"],
              "introduce": json.loads(r.text)["payload"]["items"][0]["entity"]["introduce"]}
    return json.dumps(result, ensure_ascii=False)


def star(filepath, ext):
    print("-------------------------------star------------------------------------")
    print("测试文件绝对路径：" + filepath)
    url = 'https://gwgray.tvs.qq.com/ai/image/famous'
    # 封装请求头：数据请求格式+鉴权信息
    headers = {'Content-Type': 'Content-Type: image/jpeg',
               'Appkey': AppKey}

    data = open(filepath, 'rb')
    print(type(data))
    r = requests.post(url, data=data, headers=headers)

    if not json.loads(r.text)["header"]["code"] == 200:
        result = {"status": False, "msg": json.loads(r.text)["header"]["message"]}
        return json.dumps(result, ensure_ascii=False)
    print("识别到的文字：" + json.loads(r.text)["payload"]["items"][0]["id"])  # 是将字符串传化为字典

    if json.loads(r.text)["payload"]["items"][0]["id"] == "":
        result = {"status": False,
                  "msg": "未识别到"}
        return json.dumps(result, ensure_ascii=False)
    result = {"status": True,
              "id": json.loads(r.text)["payload"]["items"][0]["id"],
              "introduce": json.loads(r.text)["payload"]["items"][0]["entity"]["introduce"]}
    return json.dumps(result, ensure_ascii=False)


def self(filepath, text, ext):
    print("-------------------------------self-------------------------------------")
    print("测试文件绝对路径：" + filepath)
    url = 'https://gwgray.tvs.qq.com/ai/predict/speech/qa-once'

    headers = {
        'Appkey': AppKey,
        'Content-Type': 'multipart/form-data;boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
        'DSN': '28:37:13:05:4A:4C'
    }
    payload = json.dumps({  # json.dumps() 是把python对象转换成json对象的一个过程，生成的是字符串
        "payload": {
            "audioMeta": {
                "format": ext,  # 音频格式: pcm/mp3
            },
            "vRefs": [text],
            "sEngine": ""
        }
    })
    data = MultipartEncoder(  # 封装的请求数据
        fields={
            "audio": (None, open(filepath, 'rb'), 'audio/' + ext),
            # form-data; name="audio"; filename="/D:/123/voiceprint.3.wav" 字段为audio,文件名的key是filename,类型是audio/mp3
            "metadata": (None, payload, "application/json; charset=utf8"),  # form-data; name="metadata"
        }, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW"
    )
    r = requests.post(url, data=data, headers=headers)
    # print(r.text)
    if not json.loads(r.text)["header"]["code"] == 200:
        result = {"status": True, "msg": json.loads(r.text)["header"]["message"]}
        return json.dumps(result, ensure_ascii=False)
    print("识别到的文字：" + json.loads(r.text)["payload"]["score"])  # 是将字符串传化为字典

    result = {"status": True,
              "score": json.loads(r.text)["payload"]["score"]}
    return json.dumps(result, ensure_ascii=False)
