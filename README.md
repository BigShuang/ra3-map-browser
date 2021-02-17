# ra3-map-browser
红警三地图浏览器

依赖第三方库
安装PIL(pillow)：
```bash
pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
```


CURRENT:
展示总地图数量

TODO:

- [x] 行列数、地图图片大小设置
- [x] 放大缩小与适配
  
- [ ] 搜索功能、 常用搜索词
- [ ] 跳转到第几页
- [ ] 获取地图人数 (不好解决，要能解析map文件)


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
