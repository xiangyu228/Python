__author__ = '井翔宇'
"""
  @ 基于百度AI的文字识别服务
  @ 识别图片中的文字信息
  @ 时间:2018-10-10 11:02
  @ 更多接口信息参见:https://ai.baidu.com/docs#/OCR-Python-SDK/07883957
"""
from aip import AipOcr
import base64

"""
  @ 初始化新建一个AipOcr
  @ 并返回结果
"""
def AipOcr_(APP_ID, API_KEY, SECRET_KEY):
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    return client

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

"""
  @ 调用通用文字识别, 图片参数为本地图片
  @ 测试发现精度不高
"""
def general_img(client,img_path):
    image = get_file_content(img_path)
    result= client.basicGeneral(image);
    return result

"""
  @ 调用通用文字识别
  @（高精度版）
"""
def basicAccurate_img(client,img_path):
    image = get_file_content(img_path)
    result= client.basicAccurate(image);
    return result

"""
  @ 调用通用文字识别, 图片参数为远程url图片
"""
def basicGeneral_img(client,img_path):
    image_path = 'https://b-ssl.duitang.com/uploads/item/201601/10/20160110133212_KUrc4.jpeg'
    result = client.basicGeneralUrl(image_path);
    return result

# 主体入口
if __name__ == '__main__':

    APP_ID = '14385953'
    API_KEY = 'SR9GY7DFqvNklUbkdBhiTADH'
    SECRET_KEY = 'Hf16YGpQzkGAvl3HEGFNt3crydt6oZs8 '

    image_path = 'img/timg.jpg'
    client = AipOcr_(APP_ID, API_KEY, SECRET_KEY)
    #general_result = general_img(client, image_path)             # 通用文字识别
    #basicAccurate_img = basicAccurate_img(client, image_path)    # 通用文字识别(高精度)
    basicGeneral_img =  basicGeneral_img(client, 'https://b-ssl.duitang.com/uploads/item/201601/10/20160110133212_KUrc4.jpeg')    # 通用文字识别(网络图片)
    print(basicGeneral_img)