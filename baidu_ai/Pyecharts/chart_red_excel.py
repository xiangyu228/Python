__author__ = '井翔宇'
"""
  @ 数据结构简单，仅供测试使用
  @ 使用读取excel文件并画图
  @ 时间:2018-10-10 13:59
"""
from pyecharts import Bar
import xlrd

def xlrd_read(file_path):
    data = xlrd.open_workbook('test.xls')  # 打开文件
    table = data.sheets()[0]               # 获取第一个sheet
    nrows = table.nrows                    # 获取表格总行数
    nclos = table.ncols                    # 获取表格总列数
    col1  = table.row_values(0)            # 获取第一行
    col2  = table.row_values(1)            # 获取第一行
    bar_chart(col1,col2)

def bar_chart(col1,col2):
    bar = Bar("我的第一个图表", "这里是副标题")
    bar.add("服装", col1, col2,is_more_utils=True)
    bar.show_config()
    bar.render('2.html')

if __name__ == '__main__':
    file = 'text.xls'
    xlrd_read(file)
