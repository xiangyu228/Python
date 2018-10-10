__author__ = '井翔宇'
"""
  @ 基于百度AI的人脸识别
  @ 识别出人脸的位置，并标记位置
  @ 时间:2018-9-29 15:42
"""

from aip import AipFace
import base64
import json
import cv2
"""
  @ 初始化AirFace对象
  @ 并返回结果
"""
def detect(APP_ID, API_KEY, SECRET_KEY, image_path, image_maxnum):
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)                # 初始化AirFace对象

    imopen = open(image_path,'rb')                               # 打开图片
    image = base64.b64encode(imopen.read())                      # 图片类型 BASE64:图片的base64值，base64编码后的图片数据，需urlencode
    image64 = str(image,'utf-8')                                 # 转换string类型
    image_type = "BASE64"                                        # 图片类型 BASE64

    # 调用人脸检测 如果有可选参数
    options = {}
    options["face_field"] = "age"
    options["max_face_num"] = image_maxnum
    options["face_type"] = "LIVE"
    result =client.detect(image64, image_type, options)
    return result

# 显示图像并标记人脸
def result_img_show(image_path,result):

    imgs = cv2.imread(image_path)                                 # 读取图像
    face_num = result['result']['face_num']                       # 人脸数量
    face_list= result['result']['face_list']                      # 人脸坐标等信息列表

    for i in range(face_num):                                     # 循环标记人脸
        location = face_list[i]['location']                       # 人脸在图片中的位置信息
        left_top = (int(location['left']), int(location['top']))  # 人脸 矩阵的左上点坐标
        right_bottom = (left_top[0] + location['width'], left_top[1] + location['height']) # 人脸矩阵的右下点坐标
        cv2.rectangle(imgs, left_top, right_bottom, (200, 100, 0), 2)
        """
        用一个最小的矩形，把找到的形状包起来
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
          参数解释:

            第一个参数：img是原图

            第二个参数：（x，y）是矩阵的左上点坐标

            第三个参数：（x+w，y+h）是矩阵的右下点坐标

            第四个参数：（0,255,0）是画线对应的rgb颜色

            第五个参数：2是所画的线的宽度
        """
    cv2.namedWindow("Image")  # 创建一个窗口
    cv2.imshow("Image", imgs) # 在窗口中显示图像
    cv2.waitKey (0)           # 如果不添最后一句，在IDLE中执行窗口直接无响应。在命令行中执行的话，则是一闪而过。
    cv2.destroyAllWindows()

# 返回结果 格式化
def pre_json(result):
    son_dicts=json.dumps(result,indent=4)
    return son_dicts

# 主体入口
if __name__ == '__main__':

    APP_ID = '14313252'
    API_KEY = 'g7bnDTUUK9SMzIsKIHMyqPTw'
    SECRET_KEY = 'sAxOW2M48QOmPUxQeEza3yYbdFyCGH0Y'

    image_path = 'img/3.jpg'
    result = detect(APP_ID, API_KEY, SECRET_KEY, image_path, 10)
    result_img_show(image_path, result)