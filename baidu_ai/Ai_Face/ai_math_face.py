__author__ = '井翔宇'
"""
  @ 基于百度AI的人脸对比技术
  @ 时间:2018-10-09 16:52
"""
from aip import AipFace
import base64
import json

""" 你的 APPID AK SK """
APP_ID = '14313252'
API_KEY = 'g7bnDTUUK9SMzIsKIHMyqPTw'
SECRET_KEY = 'sAxOW2M48QOmPUxQeEza3yYbdFyCGH0Y'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

a = base64.b64encode(open('2.jpg', 'rb').read())
b = str(a)
print(type(b))



""" 调用人脸比对 """
result_json=client.match([
    {
        'image': str(base64.b64encode(open('2.jpg', 'rb').read()),'utf-8'),
        'image_type': 'BASE64',
    },
    {
        'image': str(base64.b64encode(open('3.jpg', 'rb').read()),'utf-8'),
        'image_type': 'BASE64',
    }
]);

print(result_json)