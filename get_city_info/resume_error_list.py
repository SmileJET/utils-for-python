# encoding:utf8

from pyquery import PyQuery as pq

from info import city_info
from get_city import get_doc_from_url


if __name__ == "__main__":
    error_list_file = open('error_list.txt', 'r')
    error_list = error_list_file.readlines()
    error_list_file.close()

    error_list_file = open('error_list.txt', 'w')
    output_file = open('city.txt', 'a')

    city_queue = []
    error_citys = []

    for line in error_list:
        info = city_info()
        info.set_info(line)
        city_queue.append(info)
        error_citys.append(info.name)

    html_classes = ['.provincetr', '.citytr', '.countytr', '.towntr', '.villagetr']

    while len(city_queue) > 0:
        cur_city = city_queue.pop(0)

        print(str(cur_city.id)+'\t'+str(len(city_queue)))

        output_string = ''+str(cur_city.id)+'\t'+cur_city.code+'\t'+cur_city.name+'\t'+str(cur_city.level)+'\t'+str(cur_city.parent_id)
        if cur_city.name not in error_citys:
            output_file.write(output_string+'\n')
            output_file.flush()

        if cur_city.url is None:# or cur_city.level == 3:
            continue

        try:
            doc = get_doc_from_url(cur_city.url, timeout=None, max_retries=20)
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