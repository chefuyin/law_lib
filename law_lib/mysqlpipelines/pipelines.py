from .sql import Sql
from ..items import LawLibItem

class LawLibPipeline(object):

    def process_item(self,item,spider):
        if isinstance(item,LawLibItem):
            law_lib_url=item['law_lib_url']
            ret=Sql.select_url(law_lib_url)
            if ret[0]==1:
                print('已经存在了')
                pass
            else:
                lb_title=item['title']
                lb_publish_date=item['publish_date']
                lb_department=item['department']
                lb_law_lib_url = item['law_lib_url']
                lb_source = item['source']
                lb_publish_number= item['publish_number']
                lb_invalid_date = item['invalid_date']
                lb_content = item['content']
                Sql.insert_lawlib_data(lb_title,lb_publish_date,lb_department,lb_law_lib_url,lb_source,lb_publish_number,lb_invalid_date,lb_content)
                print('开始写入')
