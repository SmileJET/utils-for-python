# Drag Files do Event

生成一个窗口，可以将文件拖放到窗口中，读取文件的地址进行需要处理过程。

### 文件说明：

- drag_files_do_event.py 窗体主程序
- do_event.py 需要对文件处理的内容

do_event.py 包含两个方法：

| 方法名         | 输入                    |
| -------------- | ----------------------- |
| event_for_file | filename 需要处理的文件 |
| event_for_dir  | dir 需要处理的目录      |

### 运行环境：

- python 2.x or 3.x
- PyQt5

### 运行方式：

```python
python drag_files_do_event.py
```

### Demo

当前程序运行效果为删除文件功能，拖拽文件到窗口即可删除相应文件或文件夹