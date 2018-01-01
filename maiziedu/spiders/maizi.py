# -*- coding: utf-8 -*-
from maiziedu.items import MaizieduItem

import scrapy
import json
import re


class MaiziSpider(scrapy.Spider):
    name = 'maizi'
    maiziurl = 'http://www.maiziedu.com'
    
    allowed_domains = ['www.maiziedu.com']
    # start_urls = ['http://www.maiziedu.com/']
    # 重写方法
    def start_requests(self):
        return [scrapy.FormRequest(
            'http://www.maiziedu.com/user/login/',
            formdata={'account_l':'账号','password_l':'密码'},
            callback=self.after_login,      
        )]

    def after_login(self, response):
        # check login succeed before going on
        status = json.loads(response.body)['status']
        # 登录成功后爬取课程列表
        if status == 'success':
            return [scrapy.Request('http://www.maiziedu.com/course/python/',callback=self.get_course,)]

    def get_course(self,response):

        course_list = response.xpath("//div[@class='artc-bt']")
        for a in course_list:
            course={}
            # 获取课程标题
            course_title = a.xpath("./h3/a/@title").extract()
            # 获取课程url
            course_url = a.xpath("./h3/a/@href").extract()

            url = self.maiziurl + course_url[0]
            course['course_title'] = course_title[0]
            course['course_url'] = url
            # 从这里开始爬取chapter(章节)列表
            print('获取章节列表： %s：%s ' % (course['course_title'],course['course_url']))
            yield scrapy.Request(url,meta=course, callback=self.get_chapter)


    # 获取章节列表
    def get_chapter(self,response):

        # 课程列表
        c_title = response.meta['course_title']
        chapter_list = response.xpath("//ul[@style]/li")

        for ct in chapter_list:
            dd = {}
            title =ct.xpath("./*/@name").extract()
            url = ct.xpath("./*/@href").extract()

            dd['course'] = c_title
            dd['chapter'] = title[0]
            url = self.maiziurl + url[0]
            print('获取视频地址： %s：%s ' % (dd['chapter'], url))
            yield scrapy.Request(url, meta=dd, callback=self.get_video,dont_filter=True)
            # yield item

    def get_video(self,response):
        item = MaizieduItem()
        a = r'\$lessonUrl = "(.*?)"'
        video = re.findall(a, response.body.decode('utf-8'))

        course = response.meta['course']
        chapter = response.meta['chapter']

        item['course'] = course
        item['chapter'] = chapter
        item['video'] = video
        # print(chapter)
        yield item