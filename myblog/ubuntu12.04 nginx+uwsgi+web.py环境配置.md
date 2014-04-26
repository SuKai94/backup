##ubuntu12.04 nginx+uwsgi+web.py环境配置
###日期：2014.04.11
###[链接](http://1.sukai.sinaapp.com/?p=88)
----
web.py是python轻量级的web框架.其实,它有内置的web server服务器..最近尝试nginx+uwsgi部署web.py的web server,配置起来还是比较烦的,在此文章中记录下来,仅供参考.

进入正题:

1.首先确保你的ubuntu已经安装了python,web.py,nginx,uswgi.(具体方法自行百度)....你可以通过python -V,nginx -v,uwsgi --version确认你是否已经安装,以及显示出安装的版本.

2.我一般都会把我的项目建在/var/www下.先在此目录下创建文件夹apps,之后/var/www/apps目录将是我之后项目的存放目录(你也可以改成自己喜欢的目录)

<b>3.配置nginx:</b>

nginx的配置文件是放在/etc/nginx下.主配置文件是nginx.conf,还有sites-available和sites-enabled.打开nginx.conf,里面有两句话注意看:

```bash
include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;
```
它会加载conf.d文件夹里面所有的.conf文件以及sites-enabled里面所有的文件,一般,我们会修改sites-avaliable里面的配置文件,因为,sites-enabled里面的配置文件都是sites-avaliable里面对应配置文件的软链接.所以,修改sites-avaliable里面的配置文件即可.一开始里面默认有个default文件,修改default即可.

修改之后的文件内容如下:

```bash
#配置服务器
server {
        listen 8080;#监听端口,默认是80
        server_name localhost;
        location / {
               include uwsgi_params;#nginx配置与python相关参数是uwsgi-params
               uwsgi_pass 127.0.0.1:9000;
               uwsgi_param UWSGI_CHDIR /var/www/apps;#项目代码存放的目录
               uwsgi_param UWSGI_SCRIPT index;#web.py开发的web应用程序的入口代码，不要带后缀.py
               uwsgi_read_timeout 1800;
        }
}
```
<b>4.配置uwsgi:</b>

uwsgi的配置方式有很多种:命令行参数,xml文件,ini文件等等,具体参考:[这里](http://www.cnblogs.com/zhouej/archive/2012/03/25/2379646.html)

我选用的是xml文件配置.在刚才的项目目录/var/www/apps下创建配置文件:wsgi.xml(名字随意),内容如下:

```bash
<uwsgi>
    <socket>127.0.0.1:9000</socket>
    <chdir>/var/www/apps</chdir>
	<wsgi-file>index.py</wsgi-file>
	<daemonize>/var/www/apps/test.log</daemonize>
</uwsgi>
```
这是最简单的一种配置,应该都能看懂是什么意思吧

5.最后,在/var/www/apps里面加上index.py(也就是入口代码啦),内容如下:

```python
import web
urls = ('/', 'main',)

class main:
    def GET(self):
        return 'This is our test\n'

app = web.application(urls, globals())
application = app.wsgifunc()
```
6.都配置好了,下面就开始运行吧

运行之前注意把端口8080和9000的进程都kill掉.

首先运行uwsgi:  sudo uwsgi -x /var/www/apps/wsgi.xml

然后开启nginx服务器:  sudo /etc/init.d/nginx start

最后,在浏览器输入: localhost:8080,成功啦!

<b>7.启动若遇到问题,去查看一下日志:nginx的日志放在/var/log/nginx下；uwsgi的日志就是刚刚配置的/var/www/apps/test.log,学会查看日志文件有助于解决问题</b>

可能你不会一次就成功的,多看看别人的博客,理解清楚他们之间怎么合作工作的,你会发现其实很简单.
