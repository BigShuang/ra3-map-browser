# ra3-map-browser
红警三地图浏览器

### 项目介绍

大家好，我是大爽。
最近自制了一个红警三地图的浏览工具。
这个工具可以放在任何位置，双击运行。
即可快速浏览红警三地图文件夹里面的地图图片。

一眼看到总共有多少张地图
可以按左右键翻页，
双击地图图片就可以在资源管理器中, 打开到对应地图文件夹。

使用简单，看图方便。

点击设置还可以设置行列数量，和地图展示图片大小。

如果由于设置过大导致软件界面太大无法关闭与重新设置
可以通过任务管理器关闭软件。
通过删除软件同目录下的setting.json文件恢复默认设置。


### 预计添加的功能

DONE:

- [x] 行列数、地图图片大小设置
- [x] 放大缩小与适配

v1.1.0  

- [x] 名字显示不全的问题 
- [x] 搜索功能、 推荐搜索词


TODO：


- [ ] 跳转到第几页
- [ ] mod地图识别

预计需要到2.0版本再更新
- [ ] 添加备份和还原功能，方便删图和添加
- [ ] 获取地图人数 (不好解决，要能解析map文件)
解释：这个数据估计要解析map文件，但是map文件的编译方式还不是很了解。
  有朋友推荐了[OpenSAGE](https://github.com/OpenSAGE/OpenSAGE) 项目
  但是这个项目时用c#写的，我理解起来估计还有点费劲，
  这个功能可能要放在我有一定的c#基础后添加。
- [ ] 上下滑动

CURRENT:
中间莫名其妙的间距


依赖第三方库
安装PIL(pillow)：
```bash
pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
```


#### py打包exe(命令行中执行)

先安装`pyinstaller`
```bash
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
```

再在代码所在文件夹中打开命令行运行
```bash
pyinstaller -F -w gui.py
pyinstaller -F -w -i ra3.ico gui.py
```


#### 设置保存后，会保存配置信息到`setting.json`中如下
```json
{
  "size": "S",
  "c": 5,
  "r": 3
}
```
