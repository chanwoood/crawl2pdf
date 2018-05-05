# crawl2pdf

## 用法

- 安装 wkhtmltox，https://wkhtmltopdf.org/downloads.html 。安装后将 bin 目录加入到环境变量。
- 安装依赖：pip install requests bs4 pdfkit 。
- 爬取代理：python proxy.py 。
- 爬取教程并制作电子书：python lxf.py 。

## 电子书

![电子书](https://upload-images.jianshu.io/upload_images/5690299-35d35e6f383a0a12.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 思路

短时间多次爬取廖雪峰网站会封 IP，所以必须用 IP 代理池。

关于 IP 代理池，详见我这个项目：https://github.com/96chh/proxy 。

由于爬取的内容较多，所以采用多线程爬取。

制作出来的电子书还不完美，详见 issues 。

