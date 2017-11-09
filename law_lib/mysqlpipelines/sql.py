import mysql.connector
# from ...dingdian import settings
# MYSQL_HOSTS= settings.MYSQL_HOSTS
# MYSQL_USER=settings.MYSQL_USER
# MYSQL_PASSWORD=settings.MYSQL_PASSWORD
# MYSQL_DB=settings.MYSQL_DB
from ..settings import *
# MYSQL_HOSTS= MYSQL_HOSTS
# MYSQL_USER=MYSQL_USER
# MYSQL_PASSWORD=MYSQL_PASSWORD
# MYSQL_DB=MYSQL_DB

cnx= mysql.connector.connect(user=MYSQL_USER,password=MYSQL_PASSWORD,host=MYSQL_HOSTS,database=MYSQL_DB)
cur=cnx.cursor(buffered=True)

class Sql:
    @classmethod
    def insert_lawlib_data(cls,title,publish_date,department,law_lib_url,source,publish_number,invalid_date,content):
        sql='INSERT INTO lawlib_data(`title`,`publish_date`,`department`,`law_lib_url`,`source`,`publish_number`,`invalid_date`,`content`) VALUES (%(title)s,%(publish_date)s,%(department)s,%(law_lib_url)s,%(source)s,%(publish_number)s,%(invalid_date)s,%(content)s)'
        value={
            'title':title,
            'publish_date':publish_date,
            'department':department,
            'law_lib_url':law_lib_url,
            'source': source,
            'publish_number': publish_number,
            'invalid_date': invalid_date,
            'content': content
        }
        cur.execute(sql,value)
        cnx.commit()

    @classmethod
    def select_url(cls,law_lib_url):
        sql="SELECT EXISTS(SELECT 1 FROM lawlib_data WHERE law_lib_url=%(law_lib_url)s)"
        value={
            'law_lib_url':law_lib_url
        }
        cur.execute(sql,value)
        return cur.fetchall()[0]

