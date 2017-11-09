# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LawLibItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    title=scrapy.Field()
    publish_date=scrapy.Field()
    department=scrapy.Field()
    law_lib_url=scrapy.Field()
    source=scrapy.Field()
    publish_number=scrapy.Field()
    invalid_date=scrapy.Field()
    content=scrapy.Field()

#   '''
# CREATE TABLE `lawlib_data` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `title` varchar(255) DEFAULT NULL,
#   `publish_date` date DEFAULT NULL,
#   `department` varchar(255) DEFAULT NULL,
#   `law_lib_url` varchar(255) DEFAULT NULL,
#   `source` varchar(1000) DEFAULT NULL,
#   `publish_number` varchar(255) DEFAULT NULL,
#   `valid_invalid` varchar(255) DEFAULT NULL,
#   `invalid_date` date DEFAULT NULL,
#   `CONTENT` mediumtext,
#   `createdtime` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
# '''