# Classify kidney for DeepLesion

为标注出DeepLesion中的CT图像是否为kidney制作的标注软件

### 功能：

- 点击打开目录加载要处理文件的目录，可以加载已经标注过的文件（0：未处理；1：kidney；2：其他情况）

- 上一张和下一张按钮分别用来切换图像

- 点击列表中的文件名可以直接切换图像

- 点击类别后时自动切换下一张图像

- 鼠标左键点击移动图片

- 鼠标右键点击还原图片

- 鼠标滚动滑轮缩放图片

- 窗口大小改变且有父级时还原图片，否则保持不变

- 快捷键A为kidney；B为其他类别

- 快捷键UP为上一张；DOWN为下一张

  

### 运行环境：

- python 3.x
- PyQt5

```python
pip install PyQt5
```

### 运行方式：

```python
python classify_kidney_for_DeepLesion.py
```

### Demo

dir_path.json：加载过的目录

000001_01_01：存储测试图像的目录

anno_0.json：测试结果（内容纯属随机，非真实标签）

下图为程序界面

![](img/demo_1.png)

---

### 2019年1月18日 更新：

DeepLesion有单独提供key slice，里面的图像有提供转换后且标记过lesion位置的图像

- 添加按钮快捷键
- 显示当前标注进度
- 添加标签显示当前图像类别

test文件夹为key slice的部分文件

程序截图如下：

![](img/demo_2.png)