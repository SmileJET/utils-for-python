# ecoding:utf8

import time

import requests
from pyquery import PyQuery as pq
from requests.adapters import HTTPAdapter

from city_info import city_info

target_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'

# 用来获取 时间戳
def gettime():
    return int(round(time.time() * 1000))

def get_doc_from_url(target_url, timeout=5, max_retries=5):
    # 用来自定义头部的
    headers = {}
    # 用来传递参数的
    keyvalue = {}

    # 头部的填充
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) ' \
                            'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                            'Version/12.0 Safari/605.1.15'

    # 下面是参数的填充，参考图10
    keyvalue['m'] = 'QueryData'
    keyvalue['dbcode'] = 'hgnd'
    keyvalue['rowcode'] = 'zb'
    keyvalue['colcode'] = 'sj'
    keyvalue['wds'] = '[]'
    keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0301"}]'
    keyvalue['k1'] = str(gettime())

    # 建立一个Session
    s = requests.session()
    s.mount('http://', HTTPAdapter(max_retries=max_retries))
    s.mount('https://', HTTPAdapter(max_retries=max_retries))
    # 在Session基础上进行一次请求
    r = s.get(target_url, params=keyvalue, headers=headers, timeout=timeout)

    data = r.content.decode('gbk')

    doc = pq(data)
    return doc


if __name__ == "__main__":
        
    id = 0
    city_queue = []

    output_file = open('city.txt', 'w')
    error_list_file = open('error_list.txt', 'w')

    html_classes = ['.provincetr', '.citytr', '.countytr', '.towntr', '.villagetr']

    init_level = 0

    #省级别
    doc = get_doc_from_url(target_url)
    provinces = doc(html_classes[init_level]).find('a')
    for i in range(len(provinces)):
        id+=1
        href = provinces.eq(i).attr('href')
        tmp = city_info(id=id, level=0, url=target_url+href, parent_id=id)
        tmp.code = href.replace('.html', '')
        tmp.name = provinces.eq(i).text()
        city_queue.append(tmp)

    while len(city_queue) > 0:
        cur_city = city_queue.pop(0)
        output_string = ''+str(cur_city.id)+'\t'+cur_city.code+'\t'+cur_city.name+'\t'+str(cur_city.level)+'\t'+str(cur_city.parent_id)

        print(str(cur_city.id)+'\t'+str(len(city_queue)))

        output_file.write(output_string+'\n')
        output_file.flush()

        if cur_city.url is None:
        # if cur_city.url is None or cur_city.level == 3: # level 为需要爬取的级别3为4级行政区
            continue

        try:
            doc = get_doc_from_url(cur_city.url)
        except:
            error_list_file.write(output_string+'\t'+cur_city.url+'\n')
            error_list_file.flush()
            print('connect error:'+output_string)
            continue
        

        citys=doc(html_classes[cur_city.level+1])
        
        for i in range(len(citys)):
            id+=1
            tmp = city_info(id=id, parent_id=cur_city.id, level=cur_city.level+1)
            temp_url = cur_city.url
            if len(citys.eq(i).find('a'))>0:
                href = citys.eq(i).find('a').eq(0).attr('href')
                tmp.url = temp_url.replace(temp_url.split('/')[-1], href)
            else:
                tmp.url = None
            tmp.code = citys.eq(i).find('td').eq(0).text()
            if tmp.level == 4:
                name = citys.eq(i).find('td').eq(2).text()
            else:
                name = citys.eq(i).find('td').eq(1).text()
    
            if name == '市辖区':
                if cur_city.level == 0:
                    name = cur_city.name
                else:
                    name = '其他区'
            tmp.name = name
            city_queue.append(tmp)

    output_file.close()
    error_list_file.close()
