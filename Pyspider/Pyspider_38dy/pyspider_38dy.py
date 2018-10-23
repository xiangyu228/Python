#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
  @ 作 者：井翔宇
  @ 项 目:Project: 38dy
  @ 时 间:Created on 2018-10-17 16:05:57
  @ 平 台:请配合 pyspider 使用
  @ 作 用:抓取38dy.cn的所有电影分类的信息并保存到本地或者数据库中
  @ 扩 展:可配合python邮件发送、python微信接口(wxpy)
  @ 目 的:最终实现向指定用户每天发送电影资讯信息及下载地址等
  @ 其 它:可以做其它的很多事情，有兴趣了可以在研究
"""
import os
import time
import json
import urllib
import pymysql
from pyspider.libs.base_handler import *
class Handler(BaseHandler):
    crawl_config = {
    }
    # 初始化参数
    def __init__(self):
        # 电影列表
        self.film_type_dict ={
            '动作_1':'http://www.38dy.cn/a/dongzuo/',
            '喜剧_2':'http://www.38dy.cn/a/xiju/',
            '爱情_3':'http://www.38dy.cn/a/aiqing/',
            '科幻_4':'http://www.38dy.cn/a/kehuan/',
            '剧情_5':'http://www.38dy.cn/a/juqing/',
            '悬疑_6':'http://www.38dy.cn/a/xuanyi/',
            '文艺_7':'http://www.38dy.cn/a/wenyi/',
            '战争_8':'http://www.38dy.cn/a/zhanzheng/',
            '恐怖_9':'http://www.38dy.cn/a/kongbu/',
            '灾难_10':'http://www.38dy.cn/a/zainan/',
        }
        self.page_num  = 1 # 默认分页

    # Pyspider 开始
    @every(minutes=24 * 60)
    def on_start(self):
        # 遍历所有电影分类
        for key in self.film_type_dict:
            self.crawl(self.film_type_dict[key],callback=self.index_page,save = {'film_type_name':key,'film_type_url':self.film_type_dict[key]})

    # 抓取各电影分类的总页码
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        """
           @ 由于各电影分类的分页链接中有个特定的分页类型ID如:
             科幻:http://www.38dy.cn/a/kehuan/list_4_2.html
             战争:http://www.38dy.cn/a/zhanzheng/list_8_2.html
             ......
           @ 其中4,8... 代表电影分页类型ID
           @ 因此在定义电影列表时，定义好了分类链接和分页的类型ID
           @ 这里处理之后，都直接访问电影分类的第一页
           @ 作用:为了获取该电影分类的总页数
        """        
        film_type_name_s= response.save['film_type_name']   # 电影类型 名称: "动作_1"
        film_type_url = response.save['film_type_url']      # 电影类别 UEL : "http://www.38dy.cn/a/dongzuo/"
        split_film_type_name = film_type_name_s.split('_')  # 分割电影类型名称，返回电影分类名称:动作,分页类型ID:1
        film_type_name   = split_film_type_name[0]          # 电影类型名称:"动作"
        film_type_fenlei = split_film_type_name[1]          # 电影类型分页类型ID:"1"
        
        # 再次处理url，访问电影分类的第一页
        url = film_type_url + 'list_'+ film_type_fenlei +'_'+ str(self.page_num) +'.html'
        # 请求并回调以及携带参数
        self.crawl(url, callback=self.detail_page,save = {'film_type_name':film_type_name,'film_type_fenlei':film_type_fenlei,'film_type_url':film_type_url})

    # 请求分页列表
    @config(priority=2)
    def detail_page(self,response):
        film_type_name = response.save['film_type_name']     # 电影类型名称:"动作"
        film_type_fenlei = response.save['film_type_fenlei'] # 电影类型分页类型ID:"1"
        film_type_url = response.save['film_type_url']       # 电影类别 UEL
        
        # 抓取该电影类型的总页数
        page_num_list = []
        for each in response.doc('.pageinfo strong').items():
            page_num_list.append(each.text())
        total_page = page_num_list[0]  
        
        # 开始请求所有分页列表
        while self.page_num < int(total_page) :
            url = film_type_url + 'list_'+ film_type_fenlei +'_'+ str(self.page_num) +'.html'
            self.page_num += 1
            self.crawl(url, callback=self.index_fiml_body_page,save = {'film_type_name':film_type_name})

    # 访问电影信息详情页
    def index_fiml_body_page(self,response):
        film_type_name = response.save['film_type_name']
        for each in response.doc('#list a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.film_message,save = {'film_type_name':film_type_name})

    # 重新整合电影信息
    def film_message(self, response):
        film_type_name = response.save['film_type_name']         # 电影分类名称
        film_title = response.doc('#show h1').text()             # 电影标题
        file_info  = response.doc('#showinfo p').text()          # 电影简要信息
        film_img_url = response.doc('#showdesc img').attr('src') # 电影封面图url

        file_download_text = []     # 电影下载资源 文字
        file_download_ed2k = []     # 电影下载资源 ed2k
        file_download_str_text = [] # 电影下载资源 只要种子名称
        file_download_list = []     # 重新组合下载资源文字和种子链接

        # 获取电影下载资源文字及连接存入列表
        for each in response.doc('table tbody tr td').items():
            file_download_text.append(each.text())

        # 对电影下载连接进行解码(此操作可根据需要是否保留?)
        for each in response.doc('table tbody tr td a').items():
            # url 中文解码
            file_download_ed2k.append(urllib.parse.unquote(each.attr.href, encoding='utf-8', errors='replace') )

        # 分割下载资源文字及连接并把种子名称存入list
        for x in file_download_text:
            y = str(x)
            z = y.split('：')
            file_download_str_text.append(z[0])

        # 重新组合下载资源文字和种子链接
        for index,items in enumerate(file_download_str_text):
            file_download_list.append(items+':'+file_download_ed2k[index]+'\n')

        # 把电影下载信息以字符串逗号隔开存入数据库
        strs = ",";
        new_file_download_list = strs.join(file_download_list)

        # 下载图片，并保存电影的其它信息
        self.crawl(film_img_url,callback = self.film_save_info,save = {
            'film_type_name':film_type_name,
            'film_title':film_title,
            'film_img_url':film_img_url,
            'file_info':file_info,
            'file_download_list':new_file_download_list}
        )

    # 保存电影信息
    def film_save_info(self,response):
        """
          @ 操 作:关于保存电影信息及创建本地电影信息文件夹的操作
          @ 结 果:保存图片、保存电影文本信息，可以根据需要二次更改或者直接删除掉
          @ 只保留存入数据库的操作即可
        """
        film_type_name     = response.save['film_type_name']     # 电影分类名
        film_title         = response.save['film_title']         # 电影名称
        film_img_url       = response.save['film_img_url']       # 电影封面图url
        file_info          = response.save['file_info']          # 电影简介
        file_download_list = response.save['file_download_list'] # 电影下载地址
        content = response.content                               # 图片
        """
          @ 判断电影信息文件夹是否存在
          @ 存  在:写入电影信息
          @ 不存在:创建电影信息文件夹后写入电影信息
        """
        film_path = self.mkdir_filmname(film_type_name,film_title) # 创建电影信息文件夹
        """
          @ 写入电影封面图
          @ 存  在:跳过
          @ 不存在:保存图片后执行保存电影信息及写入数据库的操作
        """
        film_img_path = film_path+'/film.jpg'
        if os.path.exists(film_img_path):
            pass
        else:
            with open(film_img_path,'wb') as file:
                file.write(content) # 写入图片

            """ 电影信息写入数据库 """
            db = pymysql.connect("localhost","root","root","38dy")
            cursor = db.cursor()
            film_add_time = int(time.time())
            data = [film_type_name,film_title,film_img_url,film_img_path,file_info,str(file_download_list),film_add_time]
            try:
                cursor.execute("INSERT INTO films(film_type_name,film_title,film_img_url,film_img_path,film_body,film_download,film_add_time) VALUES (%s,%s,%s,%s,%s,%s,%s)",data)
                db.commit()
            except:
                print("提交失败",db.Error)
                db.rollback()
            """
              @ 在本地创建text写入电影基本信息
              @ 该操作可以根据需要是否保留
            """
            file_txt_path = film_path+'/film.txt'
            if os.path.exists(file_txt_path):
                pass
            else:
                with open(file_txt_path,'a',encoding='utf-8') as file:
                    file.write(file_info+'\n')

                    for x in file_download_list:
                        file.write(x)

    # 创建电影文件夹，以电影名命名
    def mkdir_filmname(self,film_type_name,film_title):
        root_path = 'd:/38dy2/';
        film_path = os.path.join(root_path,film_type_name+'/',film_title)

        if os.path.exists(film_path):
            pass
        else:
            os.makedirs(film_path)
        return film_path

