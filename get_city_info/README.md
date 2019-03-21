# Get City Info

爬取全国行政区，默认为爬取五级行政区。爬取因为网络等原因导致部分数据爬取失败，爬取失败的数据存储在error_list.txt中。

### 数据来源：

[国家统计局官网](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/)

### 运行环境：

- python 3.x
- requests
- pyquery

### 运行方式：

```python
python get_city.py
```

当有爬取失败的数据时，运行`resume_error_list.py`补全数据。

### 数据存储格式

数据存于`city.txt`中，格式为：

| id   | code       | region_name | level      | parent_id      |
| ---- | ---------- | ----------- | ---------- | -------------- |
| 编号 | 行政区编码 | 行政区名称  | 行政区级别 | 父级行政区编号 |

