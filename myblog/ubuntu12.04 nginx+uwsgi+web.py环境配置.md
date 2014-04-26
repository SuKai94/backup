##ubuntu12.04 nginx+uwsgi+web.py��������
###���ڣ�2014.04.11
###[����](http://1.sukai.sinaapp.com/?p=88)
----
web.py��python��������web���.��ʵ,�������õ�web server������..�������nginx+uwsgi����web.py��web server,�����������ǱȽϷ���,�ڴ������м�¼����,�����ο�.

��������:

1.����ȷ�����ubuntu�Ѿ���װ��python,web.py,nginx,uswgi.(���巽�����аٶ�)....�����ͨ��python -V,nginx -v,uwsgi --versionȷ�����Ƿ��Ѿ���װ,�Լ���ʾ����װ�İ汾.

2.��һ�㶼����ҵ���Ŀ����/var/www��.���ڴ�Ŀ¼�´����ļ���apps,֮��/var/www/appsĿ¼������֮����Ŀ�Ĵ��Ŀ¼(��Ҳ���Ըĳ��Լ�ϲ����Ŀ¼)

<b>3.����nginx:</b>

nginx�������ļ��Ƿ���/etc/nginx��.�������ļ���nginx.conf,����sites-available��sites-enabled.��nginx.conf,���������仰ע�⿴:

```bash
include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;
```
�������conf.d�ļ����������е�.conf�ļ��Լ�sites-enabled�������е��ļ�,һ��,���ǻ��޸�sites-avaliable����������ļ�,��Ϊ,sites-enabled����������ļ�����sites-avaliable�����Ӧ�����ļ���������.����,�޸�sites-avaliable����������ļ�����.һ��ʼ����Ĭ���и�default�ļ�,�޸�default����.

�޸�֮����ļ���������:

```bash
#���÷�����
server {
        listen 8080;#�����˿�,Ĭ����80
        server_name localhost;
        location / {
               include uwsgi_params;#nginx������python��ز�����uwsgi-params
               uwsgi_pass 127.0.0.1:9000;
               uwsgi_param UWSGI_CHDIR /var/www/apps;#��Ŀ�����ŵ�Ŀ¼
               uwsgi_param UWSGI_SCRIPT index;#web.py������webӦ�ó������ڴ��룬��Ҫ����׺.py
               uwsgi_read_timeout 1800;
        }
}
```
<b>4.����uwsgi:</b>

uwsgi�����÷�ʽ�кܶ���:�����в���,xml�ļ�,ini�ļ��ȵ�,����ο�:[����](http://www.cnblogs.com/zhouej/archive/2012/03/25/2379646.html)

��ѡ�õ���xml�ļ�����.�ڸղŵ���ĿĿ¼/var/www/apps�´��������ļ�:wsgi.xml(��������),��������:

```bash
<uwsgi>
    <socket>127.0.0.1:9000</socket>
    <chdir>/var/www/apps</chdir>
	<wsgi-file>index.py</wsgi-file>
	<daemonize>/var/www/apps/test.log</daemonize>
</uwsgi>
```
������򵥵�һ������,Ӧ�ö��ܿ�����ʲô��˼��

5.���,��/var/www/apps�������index.py(Ҳ������ڴ�����),��������:

```python
import web
urls = ('/', 'main',)

class main:
    def GET(self):
        return 'This is our test\n'

app = web.application(urls, globals())
application = app.wsgifunc()
```
6.�����ú���,����Ϳ�ʼ���а�

����֮ǰע��Ѷ˿�8080��9000�Ľ��̶�kill��.

��������uwsgi:  sudo uwsgi -x /var/www/apps/wsgi.xml

Ȼ����nginx������:  sudo /etc/init.d/nginx start

���,�����������: localhost:8080,�ɹ���!

<b>7.��������������,ȥ�鿴һ����־:nginx����־����/var/log/nginx�£�uwsgi����־���Ǹո����õ�/var/www/apps/test.log,ѧ��鿴��־�ļ������ڽ������</b>

�����㲻��һ�ξͳɹ���,�࿴�����˵Ĳ���,����������֮����ô����������,��ᷢ����ʵ�ܼ�.
