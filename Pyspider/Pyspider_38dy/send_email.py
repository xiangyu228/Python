#!/usr/bin/env python3
#coding:utf-8
"""
  @ 作 者:井翔宇
  @ 时 间:2018-10-22
  @ 作 用:可配合定时任务，按时向指定用户发送电影资讯信息
  @ 来 源:每天定时发送最新的电影资讯 >>> http://www.38dy.cn/
  @ 使 用:配合pyspider_38dy.py(抓取电影信息)使用
  @ python发送电子邮件:http://www.runoob.com/python/python-email.html
"""
import json
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 读取电影资讯信息
def get_films_info():
    # 连接数据库
    connect = pymysql.Connect(
        host='host',
        port= 'port',
        user='user',
        passwd='passwd',
        db='db',
        charset='utf8'
    )
    # 获取游标
    cursor = connect.cursor()
    """
      @ 作 用:随机查询一条电影信息
      @ 其 它:可修改为:如果发现最新电影信息可优先发送...
    """
    sql = "SELECT * FROM yf_films WHERE id >= ((SELECT MAX(id) FROM yf_films)-(SELECT MIN(id) FROM yf_films)) * RAND() + (SELECT MIN(id) FROM yf_films) LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    #print(result)
    send_email(result)

# 发送电子邮件
def send_email(film_message):
    film_type_name = film_message[1]  # 电影类别
    film_title     = film_message[2]  # 电影名
    film_img_url   = film_message[3]  # 电影封面图url
    film_img_path  = film_message[4]  # 电影封面本地图片路径
    film_body      = film_message[5]  # 电影简介
    film_download  = film_message[6]  # 电影下载信息
    film_add_time  = film_message[7]  # 抓取时间

    # 第三方 SMTP 服务
    mail_host="smtp.qq.com"           # 设置服务器
    mail_user="2270466620"            # 用户名
    mail_pass="**************"        # 口令
    sender = '2270466620@qq.com'      # 发送者
    receivers = ['981353715@qq.com','445153051@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    mail_msg = """
                    <html>
                     <head></head>
                     <body>
                      <div id="im">
                       <div id="nml">
                        <div id="dir">
                         影片类型：%s
                        </div>
                        <div id="show">
                         <h1>%s</h1>
                         <div id="showdesc">
                          <img src="%s" class="img" data-bd-imgshare-binded="1" />
                          <div>
                           <p>
                           <span>该片迅雷下载地址和剧情：</span>
                          </div>
                         </div>
                         <div class="showad" id="pad_03"></div>
                         <div id="showinfo">
                          内容由井翔宇收集并发送给您：
                          <p> %s </p>
                          <table bgcolor="#0099cc" border="0" cellpadding="10" cellspacing="1" data-darkreader-inline-bgcolor="" style="--darkreader-inline-bgcolor:#1296c1;">
                           <tbody>
                             %s
                           </tbody>
                          </table>
                          <br />
                         </div>
                         <div class="clear"></div>
                        </div>
                       </div>
                      </div>
                     </body>
                    </html>
    """
    film_body = str(film_body)                      # 转化为字符串
    film_download = str(film_download)              # 转化为字符串
    new_film_body = film_body.replace("\n","<br/>") # 处理电影简介的换行符问题
    new_film_download = film_download.split(",")    # 处理电影下载地址
    y =""
    for x in new_film_download:
         y += """
                 <tr>
			<td bgcolor="#ffffbb" style="word-break: break-all; line-height: 18px; --darkreader-inline-bgcolor:#60600f;" width="100%" data-darkreader-inline-bgcolor="">
				"""
         y +=x +"""</td>
		</tr>
         """
    mail_msg_e = mail_msg % (film_type_name,film_title,film_img_url,new_film_body,y) # 字符串替换操作
    message = MIMEText(mail_msg_e, 'html', 'utf-8')
    message['From'] = Header("井翔宇", 'utf-8')
    message['To'] =  Header("你收不收我都发~~嘿嘿", 'utf-8')
    subject = '井翔宇为您每日电影推荐!'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")

if __name__ == '__main__':
    get_films_info()


