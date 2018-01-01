# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

'''
CREATE TABLE `maiziedu`.`maizi`( `id` INT(5) NOT NULL AUTO_INCREMENT, 
                                 `course` CHAR(100), `chapter` CHAR(100), 
                                 `video` CHAR(100), 
                                 PRIMARY KEY (`id`) ) CHARSET=utf8; 
'''

def dbHandle():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        db='maiziedu',
        charset='utf8',
        use_unicode=False
    )
    return conn

class MaizieduPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = "INSERT INTO  maizi (course,chapter,video) VALUE (%s,%s,%s)"

        try:
            cursor.execute(sql,(item['course'],item['chapter'],item['video']))
            dbObject.commit()
        except Exception as e:
            print(e)
            dbObject.rollback()

        return item





