# Tornado开发菜鸟日记

- time: 2015-01-07 14:30
- tags: Tornado, Python

---

菜鸟最近学习tornado开发网站，读的书是《Introduction To Tornado》，记录一些零零碎碎

### 网站组成

![网站组成示意图](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/网站组成示意图.png)

我盗图了；图片中前台采用的`BootStrap`，后台采用`Tornado`，数据库是`MongoDB`，都是快速开发的实用性框架和数据库

### 代码编写架构

代码目录或文件的划分：

- main.py: tornado启动入口文件，包含tornado的启动流程
- settings.py: 项目配置代码放置此处
- urls.py: 放置所有用户请求连接与handler的对应关系
- init_db.py: 数据库配置以及初始化
- handlers目录: 所有handler存放位置，里面有一个父类BaseHandler，继承torando.web.RequestHandler，供其余handler继承
- static目录: 里面会包含css目录，img目录
- templates目录: 前台模板目录，里面有一个layout.html模板，供其余模板复用

### tornado模板扩展

我们会非常希望，前端代码和后端代码一样，可以进行重复使用，tornado为开发者实现这一点，通过**extends**和**block**语句来支持模板继承

扩展一个已经存在的模板，只需在模板文件的顶部加入{% extends "layout.html"%}

以及tornado的块基础，{% block header%}...{% end %}，让我们拥有了编写能够在适合地方复用模板的灵活性

### 模板转义

tornado所有的模板都已经通过tornado.escape.xhtml_escape自动转义

如何取消某处的转义？首先两种不推荐的方法：将autoescap=None传递给Application；在模板文件中加入{% autoescape None %}，前者是让全站模板都不转义，后者是让该页面不转义；推荐做法：在需要转义的简单表达语句上写成{% raw ... %}

老齐关于转义的[总结](https://github.com/qiwsir/ITArticles/blob/master/BasicPython/314.md)蛮好的

### 用户验证

着重注意**current_user**属性: 请求处理类有一个current_user属性，它同样可以在处理程序渲染的任何模板中使用，它存储了当前请求进行用户验证的标识，默认值为None。

在请求处理类中可以结合authenticated装饰器使用tornado的认证功能

在模板文件中结合if控制语句使用: {% if not current_user%}....{% end %} 或 {{ current_user["name"] }}

### 数据库操作

因为不想在项目开始设计数据库及其表，所以可以使用mongodb；而且结合[motor驱动](http://motor.readthedocs.org/en/stable/)，可以实现tornado与后台mongdb数据库之间的异步交互

推荐一个mongoDB[极简单入门教程](http://dataunion.org/?p=5572)，简单快速
