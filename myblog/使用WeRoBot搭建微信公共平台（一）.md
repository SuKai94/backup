##使用WeRoBot搭建微信公共平台（一）
###日期：2014.04.24
###[链接](http://1.sukai.sinaapp.com/?p=92)
----
WeRoBot 是一个微信机器人框架，详情请参见它的[开源代码](https://github.com/whtsky/WeRoBot)和[文档](http://werobot.readthedocs.org/en/latest/)

下面就介绍WeRoBot+SAE实现微信公共平台的搭建（我的操作平台是ubuntu）

1.首先，这里有个[WeRoBot-SAE-demo](https://github.com/whtsky/WeRoBot-SAE-demo)，我没有完全参照它上面的readme进行部署，我就介绍一下我自己的部署过程吧。

先在我的ubuntu本地建一个文件夹，在里面添加三个文件：config.yaml，index.wsgi，robot.py，内容如下：

config.yaml
```bash
name: werobot
worker: wsgi
version: 1
```

index.wsgi（这是入口代码）
```python
import sae
from robot import robot

application = sae.create_wsgi_app(robot.wsgi)
```

robot.py
```python
import os
import sys
import saekvstorage

root = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(root, 'site-packages'))

import werobot

robot = werobot.WeRoBot(token='robot', enable_session=True, session_storage=saekvstorage.SaeKVDBStorage())

@robot.handler
def echo(message):
    return 'Hello World!'
```

2.安装第三方包

首先，你得先安装sae-python-dev，执行命令：sudo pip install sae-python-dev

之后在刚刚的应用目录下执行命令命令：saecloud install werobot，完成之后你会发现你的应用目录多了site-packages文件夹，这个文件夹就存放了你刚刚安装的第三方包。

但是，安装完成并不等于能使用，我们要import里面的文件，所以需要将site-packages目录添加到搜索路径中，其实我们刚刚的robot.py里有行代码已经为我们做好这一步了：

```python
sys.path.insert(0, os.path.join(root, 'site-packages'))
```
3.现在把你的代码通过svn提交到SAE上吧。 我做好这些步骤后没能成功，SAE的debug日志报错：

IOError: [Errno 13] Permission denied: '/data1/www/htdocs/305/wetest/1/werobot_session.dat'

后来找到[解决办法](https://github.com/whtsky/WeRoBot/issues/44)

照着上面的做就可以。注意在saekvstorage.py代码中还是要将site-packages目录添加到搜索路径中，否则会出现importerror错误

完整的saekvstorage.py

```python
#coding: utf8

import os
import sys
import saekvstorage

root = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(root, 'site-packages'))

from werobot.session import SessionStorage
import sae.kvdb

class SaeKVDBStorage(SessionStorage):
    def __init__(self):
        self.kv = sae.kvdb.KVClient()

    def prefixid(self, id):
        return "WESESSION_" + str(id)

    def get(self, id):
        return self.kv.get(self.prefixid(id)) or {}

    def set(self, id, value):
        return self.kv.set(self.prefixid(id), value)

    def delete(self, id):
        return self.kv.delete(self.prefixid(id))
```
4.好的，现在应该成功了！你给微信公共平台发送任何文本消息（目前只能处理文本消息），它都只会返回“Hello World”
