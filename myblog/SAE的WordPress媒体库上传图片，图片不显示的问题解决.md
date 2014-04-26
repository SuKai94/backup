##SAE的WordPress媒体库上传图片，图片不显示的问题解决！
###日期：2014.04.04
###[链接](http://1.sukai.sinaapp.com/?p=72)
----
<b>正好马上也清明节了，在假期来之前，我的博客诞生了。</b>

虽然博客代码以及服务器部署都不是自己独立完成的。但是，我认为博客的首要目的是记录和分享，过多把精力投入到怎么优化前台，怎么实现后台，就变得轻重不分了。我也就很自然地借助了SAE下的WordPress。

首先，在SAE下按步骤安装WordPress。默认主题只有三个，想要有些特点的话，就去网上下一些主题（免费），通过SVN提交到SAE的WordPress仓库下。

1. 我的平台是ubuntu，所以第一步先安装SVN：sudo apt-get install subversion
2. 在SAE创建好WordPress 的SVN仓库后，进入本地你想要保存的目录，执行：svn co https://svn.sinaapp.com/appname
3. 之后，把你下载解压的主题文件（夹）放在刚出现的新文件夹的主题目录里面（appname/1(version number)/wp-content/themes），执行：svn add ./* ，之后svn commit -m "add new theme"
4. 输入用户名和密码，等待上传完毕就可以使用了。
5. 还有：插件的安装和主题类似，只需把所要安装的插件复制到plugins里面即可。

问题和体会：

- 并不是所有的主题都是适合的，有一些错误的可能性
- 体会了svn和git之间的相似