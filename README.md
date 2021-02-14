# ra3-map-browser
红警三地图浏览器

安装PIL(pillow)：
```bash
pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
```

TODO:

- [ ] 行列数、地图图片大小设置
- [ ] 放大缩小与适配
- [ ] 搜索功能、 常用搜索词
- [ ] 跳转到第几页
- [ ] 获取地图人数 (不好解决，要能解析map文件)

py打包exe(命令行中执行)
先安装`pyinstaller`
```bash
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
```
再在代码所在文件夹中打开命令行运行
```bash
pyinstaller -F -w gui.py
```
