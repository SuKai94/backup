# Github马拉松如何作弊？

- time: 2014-12-12 20:40
- tags: Github, Python

---

这件事起源于，我的一次重装系统。程序猿，肯定要玩ubuntu的，当时装ubuntu没有正确设置系统时间，一次github仓库提交发现，灰色格子没有点绿

排查原因：github git commit时间是根据你本地git仓库的（即ubuntu系统时间）。然后，邪恶了一下，随意改ubuntu系统时间，再git commit，发现相应日期的github灰色格子都会被点绿。实在想不出这篇博客取啥标题名，好像和github马拉松“有关”吧，就取“Github马拉松如何作弊”吧

这是我当时发现这个问题后发的微博

![github git commit时间](https://raw.githubusercontent.com/su-kaiyao/record/master/others/imgs/weibo.png)

感谢Linux中国的转发...

后来又邪恶了，准备写个python脚本，自动完成github commit“断签补签”的任务。无非就是用python执行ubuntu命令嘛，代码逻辑很简单。准备用python subprocess模块执行shell命令

这里面涉及到一个问题：使用ubuntu date命令修改时间，是需要sudo权限的，所以待会运行.py文件时，也要用sudo python xxx.py；跟着这一步，执行git push origin master命令时，为了躲避输入github用户名和密码的麻烦，需要把公钥传到github，这里必须是你ubuntu root用户的公钥，因为你刚刚是以root身份运行python文件的嘛

脚本很简单，纯粹是娱乐的目的写的，想看的话可以参考我的[github仓库](https://github.com/su-kaiyao/Python-Practice/tree/master/githubShua)
