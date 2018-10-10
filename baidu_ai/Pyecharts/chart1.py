__author__ = '井翔宇'
"""
  @ 使用Pyecharts绘制图表
  @ 时间:2018-10-10 13:46
"""
import time
import sys
from pyecharts import Bar
bar = Bar("我的第一个图表", "这里是副标题")
bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90],is_more_utils=True)
bar.show_config()
bar.render()
